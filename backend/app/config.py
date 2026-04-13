from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://bookings:changeme@localhost:5432/bookings"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "changeme"
    environment: str = "development"

    kratos_public_url: str = "http://localhost:4433"
    kratos_admin_url: str = "http://localhost:4434"

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
