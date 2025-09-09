import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://hrms_user:hrms_password@localhost:5432/hrms_db"
    
    # JWT
    JWT_SECRET: str = "your_jwt_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Server
    PORT: int = 5000
    ENVIRONMENT: str = "development"
    
    # File Upload
    UPLOAD_DIRECTORY: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # AI Screening (for future implementation)
    AI_SCREENING_ENABLED: bool = False
    AI_MODEL_PATH: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
