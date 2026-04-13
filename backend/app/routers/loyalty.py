import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.tenant import require_loyalty
from app.models.loyalty import LoyaltyCard, LoyaltyEvent, LoyaltyProgram
from app.models.tenant import Tenant
from app.schemas.loyalty import (
    LoyaltyCardRead,
    LoyaltyProgramCreate,
    LoyaltyProgramRead,
    RedeemRequest,
    StampRequest,
)

router = APIRouter()


@router.get("/programs", response_model=list[LoyaltyProgramRead])
async def list_programs(
    tenant: Tenant = Depends(require_loyalty),
    db: AsyncSession = Depends(get_db),
) -> list[LoyaltyProgram]:
    result = await db.execute(
        select(LoyaltyProgram).where(LoyaltyProgram.tenant_id == tenant.id)
    )
    return list(result.scalars().all())


@router.post("/programs", response_model=LoyaltyProgramRead, status_code=status.HTTP_201_CREATED)
async def create_program(
    data: LoyaltyProgramCreate,
    tenant: Tenant = Depends(require_loyalty),
    db: AsyncSession = Depends(get_db),
) -> LoyaltyProgram:
    program = LoyaltyProgram(tenant_id=tenant.id, **data.model_dump())
    db.add(program)
    await db.commit()
    await db.refresh(program)
    return program


@router.post("/programs/{program_id}/stamp", response_model=LoyaltyCardRead)
async def add_stamp(
    program_id: uuid.UUID,
    data: StampRequest,
    tenant: Tenant = Depends(require_loyalty),
    db: AsyncSession = Depends(get_db),
) -> LoyaltyCard:
    result = await db.execute(
        select(LoyaltyProgram).where(
            LoyaltyProgram.id == program_id, LoyaltyProgram.tenant_id == tenant.id
        )
    )
    program = result.scalar_one_or_none()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Program nije pronađen.")

    result = await db.execute(
        select(LoyaltyCard).where(
            LoyaltyCard.program_id == program_id,
            LoyaltyCard.customer_email == data.customer_email,
        )
    )
    card = result.scalar_one_or_none()
    if not card:
        card = LoyaltyCard(
            program_id=program_id,
            tenant_id=tenant.id,
            customer_email=data.customer_email,
            customer_name=data.customer_name,
        )
        db.add(card)
        await db.flush()

    card.stamp_count += data.count
    db.add(LoyaltyEvent(card_id=card.id, event_type="stamp", delta=data.count, note=data.note))
    await db.commit()
    await db.refresh(card)
    return card


@router.post("/programs/{program_id}/redeem", response_model=LoyaltyCardRead)
async def redeem_reward(
    program_id: uuid.UUID,
    data: RedeemRequest,
    tenant: Tenant = Depends(require_loyalty),
    db: AsyncSession = Depends(get_db),
) -> LoyaltyCard:
    result = await db.execute(
        select(LoyaltyProgram).where(
            LoyaltyProgram.id == program_id, LoyaltyProgram.tenant_id == tenant.id
        )
    )
    program = result.scalar_one_or_none()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Program nije pronađen.")

    result = await db.execute(
        select(LoyaltyCard).where(
            LoyaltyCard.program_id == program_id,
            LoyaltyCard.customer_email == data.customer_email,
        )
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kartica nije pronađena.")

    required = program.stamps_required or 0
    if required > 0 and card.stamp_count < required:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nedovoljno markica. Potrebno: {required}, trenutno: {card.stamp_count}.",
        )

    card.stamp_count -= required
    card.total_redeemed += 1
    db.add(LoyaltyEvent(card_id=card.id, event_type="redeem", delta=-required, note=data.note))
    await db.commit()
    await db.refresh(card)
    return card


@router.get("/cards", response_model=list[LoyaltyCardRead])
async def list_cards(
    tenant: Tenant = Depends(require_loyalty),
    db: AsyncSession = Depends(get_db),
) -> list[LoyaltyCard]:
    result = await db.execute(select(LoyaltyCard).where(LoyaltyCard.tenant_id == tenant.id))
    return list(result.scalars().all())
