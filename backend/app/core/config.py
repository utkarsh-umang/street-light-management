import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "StreetSmart"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", True)

    class Config:
        env_file = ".env"

settings = Settings()
