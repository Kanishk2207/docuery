import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() 

class Settings(BaseSettings):
    DATABASE_URL : str = os.getenv("DATABASEURL")
    MIGRATION_SCRIPT_PATH: str = "app/internal/db/migration.sql"
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "docuery-bucket-1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")  # Replace with a secure key in production
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE: str = int(os.getenv("ACCESS_TOKEN_EXPIRE", "30"))


settings = Settings()
