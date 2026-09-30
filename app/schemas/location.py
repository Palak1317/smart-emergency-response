from pydantic import BaseModel


class LocationCreate(BaseModel):
    name: str
    latitude: float | None = None
    longitude: float | None = None


class LocationResponse(BaseModel):
    id: int
    name: str
    latitude: float | None
    longitude: float | None

    class Config:
        from_attributes = True