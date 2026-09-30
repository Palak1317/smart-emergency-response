from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from app.database.database import Base


class Dispatch(Base):
    __tablename__ = "dispatches"

    id = Column(Integer, primary_key=True, index=True)

    emergency_id = Column(
        Integer,
        ForeignKey("emergencies.id"),
        nullable=False
    )

    resource_id = Column(
        Integer,
        ForeignKey("resources.id"),
        nullable=False
    )

    distance = Column(Float, nullable=True)

    estimated_time = Column(Float, nullable=True)

    status = Column(
        String(30),
        default="DISPATCHED",
        nullable=False
    )

    dispatched_at = Column(DateTime, nullable=True)
    arrived_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)