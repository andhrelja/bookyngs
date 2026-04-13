from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth import get_session
from app.models.tenant import Tenant


async def get_current_tenant(
    db: AsyncSession = Depends(get_db),
    session: dict = Depends(get_session),
) -> Tenant:
    """Resolve the tenant that owns the current Kratos identity."""
    result = await db.execute(
        select(Tenant).where(
            Tenant.owner_kratos_id == session["id"],
            Tenant.is_active.is_(True),
        )
    )
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poslovni profil nije pronađen.",
        )
    return tenant


async def require_webshop(tenant: Tenant = Depends(get_current_tenant)) -> Tenant:
    if not tenant.has_webshop:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Webshop modul nije aktivan za ovaj račun.",
        )
    return tenant


async def require_booking(tenant: Tenant = Depends(get_current_tenant)) -> Tenant:
    if not tenant.has_booking:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Booking modul nije aktivan za ovaj račun.",
        )
    return tenant


async def require_loyalty(tenant: Tenant = Depends(get_current_tenant)) -> Tenant:
    if not tenant.has_loyalty:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Loyalty modul nije aktivan za ovaj račun.",
        )
    return tenant
