"""
Application configuration settings with proper validation and security.
"""
import os
import secrets
from typing import Optional
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings with validation."""

    # API Keys
    openai_api_key: str
    ai_ml_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: Optional[str] = None

    # Application
    environment: str = "development"
    debug: bool = True
    secret_key: str = secrets.token_urlsafe(32)

    # Security
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    rate_limit_per_minute: int = 60
    session_timeout_hours: int = 24

    # Database
    database_url: Optional[str] = None

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    @validator('openai_api_key')
    def validate_openai_key(cls, v):
        if not v or v == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY must be set to a valid API key")
        return v

    @validator('supabase_url')
    def validate_supabase_url(cls, v):
        if not v or v == "your_supabase_url_here":
            raise ValueError("SUPABASE_URL must be set to a valid URL")
        if not v.startswith("https://"):
            raise ValueError("SUPABASE_URL must use HTTPS")
        return v

    @validator('environment')
    def validate_environment(cls, v):
        if v not in ["development", "staging", "production"]:
            raise ValueError("ENVIRONMENT must be development, staging, or production")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False

        # Map environment variables to field names
        fields = {
            'openai_api_key': 'OPENAI_API_KEY',
            'ai_ml_api_key': 'AI_ML_API_KEY',
            'google_api_key': 'GOOGLE_API_KEY',
            'supabase_url': 'SUPABASE_URL',
            'supabase_anon_key': 'SUPABASE_ANON_KEY',
            'supabase_service_role_key': 'SUPABASE_SERVICE_ROLE_KEY',
            'environment': 'ENVIRONMENT',
            'debug': 'DEBUG',
            'secret_key': 'SECRET_KEY',
            'cors_origins': 'CORS_ORIGINS',
            'rate_limit_per_minute': 'RATE_LIMIT_PER_MINUTE',
            'session_timeout_hours': 'SESSION_TIMEOUT_HOURS',
            'database_url': 'DATABASE_URL',
            'log_level': 'LOG_LEVEL',
            'log_file': 'LOG_FILE',
        }

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings."""
    return settings