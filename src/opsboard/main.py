from fastapi import FastAPI
from src.opsboard.routers import users, auth, projects, tasks


app = FastAPI(title="Ops Board")
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "OpsBoard API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
