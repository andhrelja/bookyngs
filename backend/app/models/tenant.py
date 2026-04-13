import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    owner_kratos_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    # Module flags — set by operator on account provisioning
    has_webshop: Mapped[bool] = mapped_column(Boolean, default=False)
    has_booking: Mapped[bool] = mapped_column(Boolean, default=False)
    has_loyalty: Mapped[bool] = mapped_column(Boolean, default=False)

    # CorvusPay sub-merchant credentials (per-tenant)
    corvus_store_id: Mapped[str | None] = mapped_column(String(64))
    corvus_secret_key: Mapped[str | None] = mapped_column(String(256))

    # Fina eRačun fiscalization (per-tenant)
    fina_oib: Mapped[str | None] = mapped_column(String(11))
    fina_certificate_path: Mapped[str | None] = mapped_column(Text)
    fina_certificate_password: Mapped[str | None] = mapped_column(String(256))

    # Widget appearance
    widget_primary_color: Mapped[str] = mapped_column(String(7), default="#1a56db")
    widget_locale: Mapped[str] = mapped_column(String(5), default="hr")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    products = relationship("Product", back_populates="tenant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="tenant", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="tenant", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="tenant", cascade="all, delete-orphan")
    loyalty_programs = relationship("LoyaltyProgram", back_populates="tenant", cascade="all, delete-orphan")
