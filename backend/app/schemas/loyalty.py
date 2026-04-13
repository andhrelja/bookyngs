import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class LoyaltyProgramCreate(BaseModel):
    name: str
    program_type: str = "stamp"
    stamps_required: int | None = None
    reward_description: str | None = None
    points_per_eur: Decimal | None = None


class LoyaltyProgramRead(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    program_type: str
    stamps_required: int | None
    reward_description: str | None
    points_per_eur: Decimal | None
    is_active: bool

    model_config = {"from_attributes": True}


class LoyaltyCardRead(BaseModel):
    id: uuid.UUID
    program_id: uuid.UUID
    customer_email: str
    customer_name: str
    stamp_count: int
    points_balance: Decimal
    total_redeemed: int
    created_at: datetime

    model_config = {"from_attributes": True}


class StampRequest(BaseModel):
    customer_email: str
    customer_name: str
    count: int = 1
    note: str | None = None


class RedeemRequest(BaseModel):
    customer_email: str
    note: str | None = None
