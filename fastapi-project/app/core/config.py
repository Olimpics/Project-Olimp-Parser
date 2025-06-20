from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    APP_NAME: str = "Document Parser Microservice"
    DEBUG: bool = False
    FILES_DIRECTORY: str = r"C:\Users\brawl\projects\microservice\fastapi-project\input_files"

    # Указываем конфигурацию Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",           # путь к .env файлу (если он есть)
        env_file_encoding="utf-8", # кодировка файла
        extra="forbid"             # запрещать неизвестные ключи из env
    )

settings = Settings()

print(f"Files directory path: {settings.FILES_DIRECTORY}")
print(f"Directory exists: {os.path.exists(settings.FILES_DIRECTORY)}")

# Если нужно, автоматически создать директорию, если ее нет:
if not os.path.exists(settings.FILES_DIRECTORY):
    os.makedirs(settings.FILES_DIRECTORY, exist_ok=True)
