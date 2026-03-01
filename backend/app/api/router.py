from fastapi import APIRouter
from app.api.routes import upload, modeling, report

api_router = APIRouter()

api_router.include_router(upload.router, prefix="/data", tags=["Data"])
api_router.include_router(modeling.router, prefix="/model", tags=["Modeling"])
api_router.include_router(report.router, prefix="/report", tags=["Report"])