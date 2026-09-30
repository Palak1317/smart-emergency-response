from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.dispatch import Dispatch
from app.models.emergency import Emergency
from app.models.resource import Resource


router = APIRouter(
    prefix="/dispatches",
    tags=["Dispatch Tracking"]
)


ALLOWED_STATUSES = {
    "DISPATCHED",
    "EN_ROUTE",
    "ARRIVED",
    "RESOLVED"
}


@router.put("/{dispatch_id}/status")
def update_dispatch_status(
    dispatch_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    status = status.upper()

    if status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid status. Use: "
                "DISPATCHED, EN_ROUTE, ARRIVED, RESOLVED"
            )
        )

    dispatch = db.query(Dispatch).filter(
        Dispatch.id == dispatch_id
    ).first()

    if not dispatch:
        raise HTTPException(
            status_code=404,
            detail="Dispatch not found"
        )

    emergency = db.query(Emergency).filter(
        Emergency.id == dispatch.emergency_id
    ).first()

    resource = db.query(Resource).filter(
        Resource.id == dispatch.resource_id
    ).first()

    if not emergency or not resource:
        raise HTTPException(
            status_code=404,
            detail="Related emergency or resource not found"
        )

    # Update dispatch status
    dispatch.status = status

    # Update related records
    if status == "DISPATCHED":

        dispatch.dispatched_at = (
            dispatch.dispatched_at or datetime.now(timezone.utc)
        )

        emergency.status = "ASSIGNED"

        resource.status = "DISPATCHED"

    elif status == "EN_ROUTE":

        emergency.status = "EN_ROUTE"

        resource.status = "BUSY"

    elif status == "ARRIVED":

        emergency.status = "IN_PROGRESS"

        resource.status = "BUSY"

        dispatch.arrived_at = datetime.now(timezone.utc)

    elif status == "RESOLVED":

        emergency.status = "RESOLVED"

        resource.status = "AVAILABLE"

        dispatch.resolved_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(dispatch)

    return {
        "message": "Dispatch status updated successfully",
        "dispatch_id": dispatch.id,
        "emergency_id": emergency.id,
        "resource_id": resource.id,
        "dispatch_status": dispatch.status,
        "emergency_status": emergency.status,
        "resource_status": resource.status
    }