import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    sku: str | None = None
    price: Decimal
    vat_rate: Decimal = Decimal("25.00")
    stock: int | None = None
    image_url: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    stock: int | None = None
    is_active: bool | None = None


class ProductRead(ProductBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int


class OrderCreate(BaseModel):
    customer_email: str
    customer_name: str
    customer_phone: str | None = None
    items: list[OrderItemCreate]


class OrderRead(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    customer_email: str
    customer_name: str
    status: str
    total: Decimal
    jir: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
