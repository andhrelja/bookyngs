import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class ResourceBase(BaseModel):
    name: str
    description: str | None = None
    resource_type: str = "accommodation"
    capacity: int = 1
    price_per_night: Decimal | None = None
    price_per_hour: Decimal | None = None
    deposit_amount: Decimal | None = None
    image_url: str | None = None


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price_per_night: Decimal | None = None
    price_per_hour: Decimal | None = None
    deposit_amount: Decimal | None = None
    is_active: bool | None = None


class ResourceRead(ResourceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ReservationCreate(BaseModel):
    resource_id: uuid.UUID
    customer_email: str
    customer_name: str
    customer_phone: str | None = None
    guests: int = 1
    check_in: date
    check_out: date
    notes: str | None = None


class ReservationRead(BaseModel):
    id: uuid.UUID
    resource_id: uuid.UUID
    customer_name: str
    customer_email: str
    guests: int
    check_in: date
    check_out: date
    total: Decimal
    status: str
    jir: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
