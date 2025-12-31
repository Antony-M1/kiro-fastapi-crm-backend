from pydantic_settings import BaseSettings
from pydantic import field_validator
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 60
    TIMEZONE: str = "UTC"
    
    @field_validator("TIMEZONE")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Validate that the timezone string is a valid IANA timezone."""
        try:
            ZoneInfo(v)
        except ZoneInfoNotFoundError:
            raise ValueError(
                f"Invalid timezone: '{v}'. Use IANA timezone format "
                "(e.g., 'UTC', 'Asia/Kolkata', 'America/New_York')"
            )
        return v
    
    class Config:
        env_file = ".env"


settings = Settings()
