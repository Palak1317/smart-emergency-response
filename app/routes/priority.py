from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.emergency import Emergency
from app.algorithms.priority_queue import EmergencyPriorityQueue


router = APIRouter(
    prefix="/priority",
    tags=["Priority Queue"]
)


@router.get("/emergencies")
def get_prioritized_emergencies(
    db: Session = Depends(get_db)
):
    emergencies = db.query(Emergency).filter(
        Emergency.status == "PENDING"
    ).all()

    priority_queue = EmergencyPriorityQueue()

    for emergency in emergencies:
        priority_queue.add_emergency(emergency)

    result = []

    while not priority_queue.is_empty():
        emergency = priority_queue.get_next_emergency()

        result.append({
            "id": emergency.id,
            "type": emergency.type,
            "severity": emergency.severity,
            "description": emergency.description,
            "location_id": emergency.location_id,
            "status": emergency.status
        })

    return {
        "count": len(result),
        "emergencies": result
    }