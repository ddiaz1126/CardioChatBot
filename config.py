from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration loaded from environment variables"""
    
    # Application
    app_name: str = "Agent Server"
    app_version: str = "0.1.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    
    # OpenAI
    openai_api_key: str
    
    # GCP (for Vertex AI)
    gcp_project_id: str = ""
    gcp_location: str = "us-central1"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()