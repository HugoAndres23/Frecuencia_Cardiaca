from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil

router = APIRouter()

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

    file_location = f"app/data/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Archivo cargado correctamente",
        "filename": file.filename
    }