from fastapi import FastAPI
import uvicorn
from app.routers.healthcheck import router as health_check

app = FastAPI()

app.include_router(health_check)