from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import booking, loyalty, tenants, webshop

app = FastAPI(
    title="Bookyngs API",
    version="0.1.0",
    docs_url="/api/docs" if settings.environment == "development" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tenants.router, prefix="/api/tenants", tags=["tenants"])
app.include_router(webshop.router, prefix="/api/webshop", tags=["webshop"])
app.include_router(booking.router, prefix="/api/booking", tags=["booking"])
app.include_router(loyalty.router, prefix="/api/loyalty", tags=["loyalty"])


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}
