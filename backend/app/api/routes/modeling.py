from fastapi import APIRouter
from app.schemas.modeling_schema import ModelingRequest
from app.services.regression_service import run_model

router = APIRouter()

@router.post("/")
def execute_model(request: ModelingRequest):

    result = run_model(request)

    return result