from pydantic import BaseModel


class ResourceCreate(BaseModel):
    name: str
    type: str
    capacity: int = 1
    location_id: int


class ResourceResponse(BaseModel):
    id: int
    name: str
    type: str
    status: str
    capacity: int
    location_id: int

    class Config:
        from_attributes = True