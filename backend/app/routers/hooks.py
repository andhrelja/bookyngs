import uuid

from fastapi import APIRouter

router = APIRouter()


@router.post("/registration")
async def on_registration(payload: dict) -> dict:
    """
    Called by Kratos after a successful registration.

    Generates an external ID and returns it so Kratos stores it
    in the identity's metadata_public.
    """
    external_id = str(uuid.uuid4())
    return {
        "identity": {
            "metadata_public": {
                "external_id": external_id,
            }
        }
    }
