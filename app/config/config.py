import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() 

class Settings(BaseSettings):
    DATABASE_URL : str = os.getenv("DATABASEURL")
    MIGRATION_SCRIPT_PATH: str = "/app/app/internal/db/migration.sql"



settings = Settings()


