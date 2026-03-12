from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.schemas.modeling_schema import ModelingRequest
from app.services.regression_service import run_model

router = APIRouter()

DATA_DIR = Path("app/data")

@router.post("/train")
def execute_model(request: ModelingRequest):
    path = DATA_DIR / request.filename

    if not path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    result = run_model(request, path)

    return result