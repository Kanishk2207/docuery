from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from app.internal.db.migration import run_migrations
from app.internal.db.postgres import get_db
from app.config.config import settings

from app.api.auth.views import router as auth_router
from app.api.document.views import router as document_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_db() as db:
        await run_migrations(db=db, script_path=settings.MIGRATION_SCRIPT_PATH)
        print(f"Migration script ran")
    yield
    print("after")


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"message": "App is healthy"}


app.include_router(auth_router)
app.include_router(document_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
