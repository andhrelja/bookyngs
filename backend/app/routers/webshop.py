import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.tenant import require_webshop
from app.models.tenant import Tenant
from app.models.webshop import Order, OrderItem, Product
from app.schemas.webshop import OrderCreate, OrderRead, ProductCreate, ProductRead, ProductUpdate

router = APIRouter()


@router.get("/products", response_model=list[ProductRead])
async def list_products(
    tenant: Tenant = Depends(require_webshop),
    db: AsyncSession = Depends(get_db),
) -> list[Product]:
    result = await db.execute(
        select(Product).where(Product.tenant_id == tenant.id, Product.is_active.is_(True))
    )
    return list(result.scalars().all())


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    tenant: Tenant = Depends(require_webshop),
    db: AsyncSession = Depends(get_db),
) -> Product:
    product = Product(tenant_id=tenant.id, **data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@router.patch("/products/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    tenant: Tenant = Depends(require_webshop),
    db: AsyncSession = Depends(get_db),
) -> Product:
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.tenant_id == tenant.id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proizvod nije pronađen.")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: uuid.UUID,
    tenant: Tenant = Depends(require_webshop),
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.tenant_id == tenant.id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proizvod nije pronađen.")
    product.is_active = False
    await db.commit()


@router.get("/orders", response_model=list[OrderRead])
async def list_orders(
    tenant: Tenant = Depends(require_webshop),
    db: AsyncSession = Depends(get_db),
) -> list[Order]:
    result = await db.execute(
        select(Order).where(Order.tenant_id == tenant.id).order_by(Order.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("/orders", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    tenant: Tenant = Depends(require_webshop),
    db: AsyncSession = Depends(get_db),
) -> Order:
    total = Decimal("0.00")
    resolved: list[tuple[Product, int]] = []

    for item in data.items:
        result = await db.execute(
            select(Product).where(
                Product.id == item.product_id,
                Product.tenant_id == tenant.id,
                Product.is_active.is_(True),
            )
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proizvod {item.product_id} nije pronađen.",
            )
        total += product.price * item.quantity
        resolved.append((product, item.quantity))

    order = Order(
        tenant_id=tenant.id,
        customer_email=data.customer_email,
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        total=total,
        status="pending",
    )
    db.add(order)
    await db.flush()

    for product, qty in resolved:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=qty,
                unit_price=product.price,
                vat_rate=product.vat_rate,
            )
        )

    await db.commit()
    await db.refresh(order)
    return order
