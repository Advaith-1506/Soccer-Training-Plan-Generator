import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    env: str = Field(default=os.getenv("APP_ENV", "dev"))
    database_url: str = Field(default=os.getenv("DATABASE_URL", "sqlite:///soccer.db"))
    api_host: str = Field(default=os.getenv("API_HOST", "127.0.0.1"))
    api_port: int = Field(default=int(os.getenv("API_PORT", "8000")))


settings = Settings()
