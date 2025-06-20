from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    APP_NAME: str = "Document Parser Microservice"
    DEBUG: bool = False
    FILES_DIRECTORY: str = r"C:\Users\brawl\projects\microservice\fastapi-project\input_files"
    # Add these fields explicitly
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your_secret_key"

    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid"
    )

settings = Settings()

print(f"Files directory path: {settings.FILES_DIRECTORY}")
print(f"Directory exists: {os.path.exists(settings.FILES_DIRECTORY)}")

# Create directory if it doesn't exist
if not os.path.exists(settings.FILES_DIRECTORY):
    os.makedirs(settings.FILES_DIRECTORY, exist_ok=True)