import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Resource(Base):
    """A bookable resource — apartment, room, bike, boat, guided tour slot, etc."""

    __tablename__ = "resources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    # accommodation | rental | service
    resource_type: Mapped[str] = mapped_column(String(32), default="accommodation")
    capacity: Mapped[int] = mapped_column(Integer, default=1)
    price_per_night: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    price_per_hour: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    deposit_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    image_url: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tenant = relationship("Tenant", back_populates="resources")
    reservations = relationship("Reservation", back_populates="resource", cascade="all, delete-orphan")


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resources.id"), nullable=False)

    customer_email: Mapped[str] = mapped_column(String(256), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(256), nullable=False)
    customer_phone: Mapped[str | None] = mapped_column(String(32))
    guests: Mapped[int] = mapped_column(Integer, default=1)

    check_in: Mapped[date] = mapped_column(Date, nullable=False)
    check_out: Mapped[date] = mapped_column(Date, nullable=False)

    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    deposit_paid: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))

    # pending → confirmed → completed | cancelled
    status: Mapped[str] = mapped_column(String(32), default="pending")

    # Fina eRačun
    jir: Mapped[str | None] = mapped_column(String(64))
    zki: Mapped[str | None] = mapped_column(String(64))
    fiscal_number: Mapped[int | None] = mapped_column(Integer)
    fiscalized_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # CorvusPay
    corvus_order_id: Mapped[str | None] = mapped_column(String(64))

    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    tenant = relationship("Tenant", back_populates="reservations")
    resource = relationship("Resource", back_populates="reservations")
