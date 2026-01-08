from pydantic import AnyHttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union


class Settings(BaseSettings):
    PROJECT_NAME: str = "VibeFinance API"
    ENVIRONMENT: str = "development"

    # Security - No defaults to force environment variable configuration
    # These will raise a ValidationError if not found in the environment
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Encryption - Key for Application Level Encryption (ALE)
    ENCRYPTION_KEY: SecretStr

    # Database
    DATABASE_URL: str

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", extra="ignore"
    )


def get_settings() -> Settings:
    """
    Factory function to provide settings via Dependency Injection.
    Ensures we don't rely on a global settings instance.
    """
    return Settings()
