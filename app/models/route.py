from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database.database import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)

    source_location_id = Column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False
    )

    destination_location_id = Column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False
    )

    distance = Column(Float, nullable=False)