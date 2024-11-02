from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.internal.db.migration import run_migrations
from app.internal.db.postgres import get_db
from app.config.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_db() as db:
        await run_migrations(db=db, script_path=settings.MIGRATION_SCRIPT_PATH)
        print(f"Migration script ran")
    yield
    print("after")


app = FastAPI(lifespan=lifespan)


app.get("/health")
def health_check():
    return {"message": "App is healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )