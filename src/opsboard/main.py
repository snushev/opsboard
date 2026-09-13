from fastapi import FastAPI
from src.opsboard.routers import users
from src.opsboard.routers import auth


app = FastAPI(title="Ops Board")
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "OpsBoard API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
