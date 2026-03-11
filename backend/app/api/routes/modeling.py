from fastapi import APIRouter
from app.schemas.modeling_schema import ModelingRequest
from app.services.regression_service import run_model

router = APIRouter()

@router.post("/train")
def execute_model(request: ModelingRequest):
    path = f"app/data/{request.filename}"

    if not open(path):
        return {"error": "Archivo no encontrado"}

    result = run_model(request, path)

    return result