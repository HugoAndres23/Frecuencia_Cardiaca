from pydantic import BaseModel

class ModelingRequest(BaseModel):
    filename: str
    activity: str
    model_type: str
    degree: int | None = None


class ReportRequest(BaseModel):
    filename: str
    activity: str
    degree: int = 2
    algorithms: list[str] | None = None