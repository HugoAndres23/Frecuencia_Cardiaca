from fastapi import APIRouter, UploadFile, File
import shutil

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    
    file_location = f"app/data/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Archivo cargado correctamente",
        "filename": file.filename
    }