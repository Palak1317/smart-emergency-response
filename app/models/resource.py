from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(30), default="AVAILABLE", nullable=False)
    capacity = Column(Integer, default=1)

    location_id = Column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False
    )