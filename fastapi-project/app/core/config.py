from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Document Parser Microservice"
    DEBUG: bool = False
    UPLOAD_FOLDER: str = "temp_uploads"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()