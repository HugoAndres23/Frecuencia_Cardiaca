from pydantic import BaseModel

class ModelingRequest(BaseModel):
    filename: str
    activity: str
    model_type: str
    degree: int | None = None