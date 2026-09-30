from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.emergency import Emergency
from app.models.location import Location
from app.models.user import User
from app.schemas.emergency import (
    EmergencyCreate,
    EmergencyResponse
)


router = APIRouter(
    prefix="/emergencies",
    tags=["Emergencies"]
)


@router.post("/", response_model=EmergencyResponse)
def create_emergency(
    emergency: EmergencyCreate,
    db: Session = Depends(get_db)
):
    location = db.query(Location).filter(
        Location.id == emergency.location_id
    ).first()

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Location not found"
        )

    if emergency.reported_by is not None:
        user = db.query(User).filter(
            User.id == emergency.reported_by
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    new_emergency = Emergency(
        type=emergency.type,
        severity=emergency.severity,
        description=emergency.description,
        location_id=emergency.location_id,
        reported_by=emergency.reported_by
    )

    db.add(new_emergency)
    db.commit()
    db.refresh(new_emergency)

    return new_emergency


@router.get("/", response_model=list[EmergencyResponse])
def get_emergencies(
    db: Session = Depends(get_db)
):
    return db.query(Emergency).all()