import httpx
from fastapi import HTTPException, Request, status

from app.config import settings


async def get_session(request: Request) -> dict:
    """
    Extract and validate an Ory Kratos session from the incoming request.

    In production Oathkeeper sits in front of the API and injects
    X-Kratos-Authenticated-Identity-Id after validating the session cookie.
    In development we fall back to calling Kratos directly.
    """
    identity_id = request.headers.get("X-Kratos-Authenticated-Identity-Id")
    if identity_id:
        return {"id": identity_id}

    # Dev fallback: validate cookie with Kratos
    session_cookie = request.cookies.get("ory_kratos_session")
    if not session_cookie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nije autoriziran.")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.kratos_public_url}/sessions/whoami",
            cookies={"ory_kratos_session": session_cookie},
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesija nije valjana.")

    data = resp.json()
    return {"id": data["identity"]["id"], "traits": data["identity"].get("traits", {})}
