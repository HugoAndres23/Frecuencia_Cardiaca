from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import pandas as pd

router = APIRouter()

DATA_DIR = Path("app/data")


def _resolve_dataset_path(filename: str) -> Path:
    dataset_path = (DATA_DIR / filename).resolve()
    data_dir_resolved = DATA_DIR.resolve()

    if data_dir_resolved not in dataset_path.parents or not dataset_path.is_file():
        raise HTTPException(status_code=404, detail="Dataset no encontrado")

    return dataset_path


@router.get("/files")
def list_csv_files():
    files = sorted(
        file_path.name
        for file_path in DATA_DIR.glob("*.csv")
        if file_path.is_file()
    )

    return {"files": files}


@router.get("/activities")
def list_dataset_activities(filename: str):
    dataset_path = _resolve_dataset_path(filename)
    df = pd.read_csv(dataset_path)

    if "actividad" not in df.columns:
        raise HTTPException(status_code=400, detail="La columna 'actividad' no existe en el dataset")

    activities = sorted(
        {
            str(activity).strip()
            for activity in df["actividad"].dropna().tolist()
            if str(activity).strip()
        }
    )

    return {"activities": activities}

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
   
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos CSV"
        )
    
    if file.content_type not in ['text/csv', 'application/vnd.ms-excel']:
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser un CSV válido"
        )

    file_location = DATA_DIR / file.filename

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Archivo cargado correctamente",
        "filename": file.filename
    }