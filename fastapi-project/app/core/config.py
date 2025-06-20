from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Document Parser Microservice"
    DEBUG: bool = True
    FILES_DIRECTORY: str = str(BASE_DIR / "input_files")
    UPLOAD_FOLDER: str = str(BASE_DIR / "uploads")
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your_secret_key"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
        env_prefix=""
    )

print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Base directory: {BASE_DIR}")

try:
    settings = Settings()
    
    env_files_dir = os.environ.get("FILES_DIRECTORY")
    if env_files_dir:
        settings.FILES_DIRECTORY = env_files_dir
        print(f"Overriding FILES_DIRECTORY from environment variable: {settings.FILES_DIRECTORY}")

    env_upload_folder = os.environ.get("UPLOAD_FOLDER")
    if env_upload_folder:
        settings.UPLOAD_FOLDER = env_upload_folder
        print(f"Overriding UPLOAD_FOLDER from environment variable: {settings.UPLOAD_FOLDER}")
    
    print(f"Settings loaded successfully")
    print(f"DEBUG mode: {settings.DEBUG}")
    print(f"FILES_DIRECTORY: {settings.FILES_DIRECTORY}")
    print(f"UPLOAD_FOLDER: {settings.UPLOAD_FOLDER}")
    
    for directory in [settings.FILES_DIRECTORY, settings.UPLOAD_FOLDER]:
        print(f"Checking directory: {directory}")
        print(f"Directory exists: {os.path.exists(directory)}")
        
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"Created directory: {directory}")
            except Exception as e:
                print(f"Error creating directory {directory}: {e}")
                
                import tempfile
                temp_dir = tempfile.gettempdir()
                alt_dir = os.path.join(temp_dir, os.path.basename(directory))
                print(f"Trying alternative directory: {alt_dir}")
                os.makedirs(alt_dir, exist_ok=True)
                
                if directory == settings.FILES_DIRECTORY:
                    settings.FILES_DIRECTORY = alt_dir
                elif directory == settings.UPLOAD_FOLDER:
                    settings.UPLOAD_FOLDER = alt_dir
                    
                print(f"Using alternative directory: {alt_dir}")
    
    for directory in [settings.FILES_DIRECTORY, settings.UPLOAD_FOLDER]:
        try:
            test_file_path = os.path.join(directory, "test_write.txt")
            with open(test_file_path, "w") as f:
                f.write("Test write access")
            os.remove(test_file_path)
            print(f"Write access to {directory} confirmed")
        except Exception as e:
            print(f"Warning: Cannot write to directory {directory}: {e}")
            
            import tempfile
            temp_dir = tempfile.gettempdir()
            alt_dir = os.path.join(temp_dir, os.path.basename(directory))
            print(f"Trying alternative directory for writing: {alt_dir}")
            os.makedirs(alt_dir, exist_ok=True)
            
            if directory == settings.FILES_DIRECTORY:
                settings.FILES_DIRECTORY = alt_dir
            elif directory == settings.UPLOAD_FOLDER:
                settings.UPLOAD_FOLDER = alt_dir
                
            print(f"Using alternative directory for writing: {alt_dir}")

except Exception as e:
    print(f"Error loading settings: {e}")
    class FallbackSettings:
        APP_NAME = "Document Parser Microservice"
        DEBUG = True
        FILES_DIRECTORY = str(BASE_DIR / "input_files")
        UPLOAD_FOLDER = str(BASE_DIR / "uploads")
        database_url = "sqlite:///./test.db"
        secret_key = "default_fallback_key"
    
    settings = FallbackSettings()
    print(f"Using fallback settings")
    
    for directory in [settings.FILES_DIRECTORY, settings.UPLOAD_FOLDER]:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"Created directory: {directory}")
            except Exception as e:
                print(f"Error creating directory {directory}: {e}")
                
                import tempfile
                temp_dir = tempfile.gettempdir()
                alt_dir = os.path.join(temp_dir, os.path.basename(directory))
                os.makedirs(alt_dir, exist_ok=True)
                
                if directory == settings.FILES_DIRECTORY:
                    settings.FILES_DIRECTORY = alt_dir
                elif directory == settings.UPLOAD_FOLDER:
                    settings.UPLOAD_FOLDER = alt_dir
                    
                print(f"Using temporary directory: {alt_dir}")