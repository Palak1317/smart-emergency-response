from datetime import datetime

from pydantic import BaseModel


class EmergencyCreate(BaseModel):
    type: str
    severity: str
    description: str | None = None
    location_id: int
    reported_by: int | None = None


class EmergencyResponse(BaseModel):
    id: int
    type: str
    severity: str
    description: str | None
    status: str
    location_id: int
    reported_by: int | None
    created_at: datetime

    class Config:
        from_attributes = True