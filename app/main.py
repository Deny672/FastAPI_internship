from fastapi import FastAPI
import uvicorn
from app.routers.healthcheck import router as health_check

app = FastAPI()

app.include_router(health_check)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)