from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Document Parser Microservice"
    DEBUG: bool = False
    FILES_DIRECTORY: str = str(BASE_DIR / "input_files")
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your_secret_key"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid"
    )

settings = Settings()

print(f"Files directory path: {settings.FILES_DIRECTORY}")
print(f"Directory exists: {os.path.exists(settings.FILES_DIRECTORY)}")

if not os.path.exists(settings.FILES_DIRECTORY):
    os.makedirs(settings.FILES_DIRECTORY, exist_ok=True)