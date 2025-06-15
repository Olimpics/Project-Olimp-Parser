from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    APP_NAME: str = "Document Parser Microservice"
    DEBUG: bool = False
    FILES_DIRECTORY: str = r"C:\Users\brawl\projects\microservice\fastapi-project\input_files"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

print(f"Files directory path: {settings.FILES_DIRECTORY}")
print(f"Directory exists: {os.path.exists(settings.FILES_DIRECTORY)}")