"""
CorvusPay payment gateway integration.

CorvusPay operates on a sub-merchant model: each tenant has their own store ID
and secret key obtained directly from CorvusPay. The platform integrates the
payment flow on their behalf.

This module is a stub. Production implementation requires:
  - CorvusPay merchant agreement per tenant
  - Correct HMAC-SHA256 signature construction per CorvusPay spec
  - Handling of CorvusPay callback/webhook for payment confirmation

Currency: EUR (Croatia adopted EUR on 1 Jan 2023).
"""

import hashlib
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class CorvusPayError(Exception):
    pass


def _sign(store_id: str, amount_cents: int, order_id: str, secret_key: str) -> str:
    """Compute HMAC-SHA256 signature over canonical field string."""
    raw = f"{store_id}{amount_cents}{order_id}{secret_key}"
    return hashlib.sha256(raw.encode()).hexdigest()


async def create_payment(
    *,
    store_id: str,
    secret_key: str,
    order_id: str,
    amount: Decimal,
    currency: str = "EUR",
    language: str = "hr",
    success_url: str,
    cancel_url: str,
) -> dict[str, str]:
    """
    Initiate a CorvusPay hosted payment session.

    Returns:
        {"redirect_url": str, "corvus_order_id": str}

    The caller must redirect the customer to redirect_url to complete payment.
    After payment CorvusPay will POST to the configured callback URL.

    Raises:
        CorvusPayError: if the CorvusPay API returns an error.
    """
    amount_cents = int(amount * 100)
    _sign(store_id, amount_cents, order_id, secret_key)

    # TODO: POST to CorvusPay API to create session and receive redirect URL
    logger.warning("CorvusPay stub — no real payment initiated. order_id: %s", order_id)

    return {
        "redirect_url": f"https://stub.corvuspay.com/pay/{order_id}",
        "corvus_order_id": order_id,
    }


async def verify_callback(*, store_id: str, secret_key: str, payload: dict) -> bool:
    """
    Verify the signature on a CorvusPay payment callback.

    Must be called before marking an order as paid.
    """
    # TODO: implement CorvusPay callback signature verification
    logger.warning("CorvusPay callback verification stub — always returns True.")
    return True
