from fastapi import FastAPI
from app.api.v1 import auth, tasks
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])


@app.get("/healthcheck", tags=["system"])
async def healthcheck():
    return {"status": "ok"}
