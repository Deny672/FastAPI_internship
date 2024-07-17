from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.healthcheck import router as health_check
from app.routers.user import router as user

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user)
app.include_router(health_check)