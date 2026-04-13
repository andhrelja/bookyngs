from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.tenant import get_current_tenant
from app.models.tenant import Tenant
from app.schemas.tenant import TenantRead, TenantUpdate

router = APIRouter()


@router.get("/me", response_model=TenantRead)
async def get_my_tenant(tenant: Tenant = Depends(get_current_tenant)) -> Tenant:
    return tenant


@router.patch("/me", response_model=TenantRead)
async def update_my_tenant(
    data: TenantUpdate,
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db),
) -> Tenant:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(tenant, field, value)
    await db.commit()
    await db.refresh(tenant)
    return tenant
