from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.resource import Resource
from app.models.location import Location
from app.schemas.resource import ResourceCreate, ResourceResponse


router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


@router.post("/", response_model=ResourceResponse)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db)
):
    location = db.query(Location).filter(
        Location.id == resource.location_id
    ).first()

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Location not found"
        )

    new_resource = Resource(
        name=resource.name,
        type=resource.type,
        capacity=resource.capacity,
        location_id=resource.location_id
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource


@router.get("/", response_model=list[ResourceResponse])
def get_resources(
    db: Session = Depends(get_db)
):
    return db.query(Resource).all()