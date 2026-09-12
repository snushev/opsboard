from fastapi import FastAPI
from src.opsboard.routers import users
from src.opsboard.core.database import engine
from src.opsboard.core.base import Base


app = FastAPI(title="Ops Board")
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "OpsBoard API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
