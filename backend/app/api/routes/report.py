from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.modeling_schema import ReportRequest
from app.services.pdf_service import generate_pdf
from app.services.regression_service import run_models_for_report

router = APIRouter()

DATA_DIR = Path("app/data")


@router.post("/pdf")
def create_pdf_report(request: ReportRequest):
    file_path = DATA_DIR / request.filename

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Dataset no encontrado")

    try:
        results = run_models_for_report(
            path=file_path,
            activity=request.activity,
            degree=request.degree,
            algorithms=request.algorithms,
        )
        pdf_stream = generate_pdf(results, filename=request.filename, activity=request.activity)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=reporte_{request.filename.replace('.csv', '')}.pdf"
        },
    )