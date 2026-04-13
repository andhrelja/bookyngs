import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.tenant import require_booking
from app.models.booking import Reservation, Resource
from app.models.tenant import Tenant
from app.schemas.booking import (
    ReservationCreate,
    ReservationRead,
    ResourceCreate,
    ResourceRead,
    ResourceUpdate,
)

router = APIRouter()


@router.get("/resources", response_model=list[ResourceRead])
async def list_resources(
    tenant: Tenant = Depends(require_booking),
    db: AsyncSession = Depends(get_db),
) -> list[Resource]:
    result = await db.execute(
        select(Resource).where(Resource.tenant_id == tenant.id, Resource.is_active.is_(True))
    )
    return list(result.scalars().all())


@router.post("/resources", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
async def create_resource(
    data: ResourceCreate,
    tenant: Tenant = Depends(require_booking),
    db: AsyncSession = Depends(get_db),
) -> Resource:
    resource = Resource(tenant_id=tenant.id, **data.model_dump())
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


@router.patch("/resources/{resource_id}", response_model=ResourceRead)
async def update_resource(
    resource_id: uuid.UUID,
    data: ResourceUpdate,
    tenant: Tenant = Depends(require_booking),
    db: AsyncSession = Depends(get_db),
) -> Resource:
    result = await db.execute(
        select(Resource).where(Resource.id == resource_id, Resource.tenant_id == tenant.id)
    )
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resurs nije pronađen.")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    await db.commit()
    await db.refresh(resource)
    return resource


@router.get("/reservations", response_model=list[ReservationRead])
async def list_reservations(
    tenant: Tenant = Depends(require_booking),
    db: AsyncSession = Depends(get_db),
) -> list[Reservation]:
    result = await db.execute(
        select(Reservation)
        .where(Reservation.tenant_id == tenant.id)
        .order_by(Reservation.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("/reservations", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    data: ReservationCreate,
    tenant: Tenant = Depends(require_booking),
    db: AsyncSession = Depends(get_db),
) -> Reservation:
    result = await db.execute(
        select(Resource).where(
            Resource.id == data.resource_id,
            Resource.tenant_id == tenant.id,
            Resource.is_active.is_(True),
        )
    )
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resurs nije pronađen.")

    nights = (data.check_out - data.check_in).days
    if nights <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Datum odjave mora biti nakon datuma prijave.",
        )

    price = resource.price_per_night or Decimal("0.00")
    total = price * nights

    reservation = Reservation(
        tenant_id=tenant.id,
        resource_id=resource.id,
        customer_email=data.customer_email,
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        guests=data.guests,
        check_in=data.check_in,
        check_out=data.check_out,
        total=total,
        notes=data.notes,
        status="pending",
    )
    db.add(reservation)
    await db.commit()
    await db.refresh(reservation)
    return reservation


@router.patch("/reservations/{reservation_id}/status")
async def update_reservation_status(
    reservation_id: uuid.UUID,
    new_status: str,
    tenant: Tenant = Depends(require_booking),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    valid = {"pending", "confirmed", "cancelled", "completed"}
    if new_status not in valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nevažeći status.")
    result = await db.execute(
        select(Reservation).where(
            Reservation.id == reservation_id, Reservation.tenant_id == tenant.id
        )
    )
    reservation = result.scalar_one_or_none()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rezervacija nije pronađena.")
    reservation.status = new_status
    await db.commit()
    return {"status": new_status}
