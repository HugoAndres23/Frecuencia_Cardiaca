from fastapi import FastAPI
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import ALLOWED_ORIGINS

app = FastAPI(
    title="Heart Rate Modeling API",
    description="API para modelamiento de frecuencia cardíaca",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)