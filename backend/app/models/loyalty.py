import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class LoyaltyProgram(Base):
    __tablename__ = "loyalty_programs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    # stamp | points
    program_type: Mapped[str] = mapped_column(String(16), default="stamp")
    stamps_required: Mapped[int | None] = mapped_column(Integer)
    reward_description: Mapped[str | None] = mapped_column(Text)
    points_per_eur: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    tenant = relationship("Tenant", back_populates="loyalty_programs")
    cards = relationship("LoyaltyCard", back_populates="program", cascade="all, delete-orphan")


class LoyaltyCard(Base):
    __tablename__ = "loyalty_cards"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loyalty_programs.id"), nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    customer_email: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    customer_name: Mapped[str] = mapped_column(String(256), nullable=False)
    stamp_count: Mapped[int] = mapped_column(Integer, default=0)
    points_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    total_redeemed: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    program = relationship("LoyaltyProgram", back_populates="cards")
    events = relationship("LoyaltyEvent", back_populates="card", cascade="all, delete-orphan")


class LoyaltyEvent(Base):
    """Immutable audit log: stamps given, points awarded, rewards redeemed."""

    __tablename__ = "loyalty_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("loyalty_cards.id"), nullable=False)
    # stamp | points | redeem
    event_type: Mapped[str] = mapped_column(String(16), nullable=False)
    delta: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    note: Mapped[str | None] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    card = relationship("LoyaltyCard", back_populates="events")
