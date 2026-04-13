"""
Fina eRačun fiscalization service.

Every payment in Croatia must be fiscalized via the Fina API (Porezna uprava CIS).
The API returns a JIR (Jedinstveni identifikator računa) which must appear on the
issued receipt. This is legally mandatory for all paying tenants.

This module is a stub. Production implementation requires:
  1. A valid Fina certificate (.p12) per tenant
  2. ZKI (Zaštitni kod izdavatelja) computation — MD5 of signed key fields
  3. A SOAP request to the Fina CIS endpoint, signed with the certificate
  4. Parsing the JIR from the SOAP response

Relevant resources:
  - Zakon o fiskalizaciji u prometu gotovinom (NN 133/12, 115/16, 106/18)
  - Fina tehničke specifikacije: https://www.fina.hr/fiskalizacija
  - CIS test endpoint: https://cistest.apis-it.hr:8449/FiskalizacijaServiceTest
  - CIS prod endpoint: https://cis.porezna-uprava.hr:8449/FiskalizacijaService
"""

import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class FiscalizationError(Exception):
    pass


async def fiscalize_invoice(
    *,
    tenant_oib: str,
    certificate_path: str,
    certificate_password: str,
    amount: Decimal,
    vat_amount: Decimal,
    invoice_number: int,
    operator_oib: str,
    payment_method: str = "K",  # G=gotovina, K=kartica, T=transakcijski račun
) -> dict[str, str]:
    """
    Submit an invoice to Fina CIS and return the JIR and ZKI.

    Returns:
        {"jir": str, "zki": str}

    Raises:
        FiscalizationError: if the Fina API rejects the request.
    """
    # TODO: implement actual Fina SOAP/REST call
    # Steps:
    # 1. Load PKCS12 certificate from certificate_path
    # 2. Compute ZKI = MD5(oib + datetime + br_rac + iznos + tajni_ključ)
    # 3. Build FiskalizacijaRacunaZahtjev SOAP envelope
    # 4. Sign envelope with certificate (XMLDSig)
    # 5. POST to CIS endpoint with mutual TLS
    # 6. Parse JIR from FiskalizacijaRacunaOdgovor
    logger.warning(
        "Fiscalization stub — no real API call made. OIB: %s, amount: %s, invoice: %s",
        tenant_oib,
        amount,
        invoice_number,
    )
    return {
        "jir": f"STUB-JIR-{invoice_number:08d}",
        "zki": f"STUB-ZKI-{invoice_number:08d}",
    }
