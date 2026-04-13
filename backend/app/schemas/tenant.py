import uuid
from datetime import datetime

from pydantic import BaseModel


class TenantBase(BaseModel):
    name: str
    slug: str
    widget_primary_color: str = "#1a56db"
    widget_locale: str = "hr"


class TenantCreate(TenantBase):
    owner_kratos_id: str


class TenantUpdate(BaseModel):
    name: str | None = None
    widget_primary_color: str | None = None
    widget_locale: str | None = None
    corvus_store_id: str | None = None
    corvus_secret_key: str | None = None
    fina_oib: str | None = None


class TenantRead(TenantBase):
    id: uuid.UUID
    has_webshop: bool
    has_booking: bool
    has_loyalty: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
