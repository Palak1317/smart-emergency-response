from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.location import Location
from app.models.route import Route
from app.algorithms.graph import Graph


router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)


@router.post("/")
def create_route(
    source_location_id: int,
    destination_location_id: int,
    distance: float,
    db: Session = Depends(get_db)
):

    source = db.query(Location).filter(
        Location.id == source_location_id
    ).first()

    destination = db.query(Location).filter(
        Location.id == destination_location_id
    ).first()

    if not source:
        raise HTTPException(
            status_code=404,
            detail="Source location not found"
        )

    if not destination:
        raise HTTPException(
            status_code=404,
            detail="Destination location not found"
        )

    new_route = Route(
        source_location_id=source_location_id,
        destination_location_id=destination_location_id,
        distance=distance
    )

    db.add(new_route)
    db.commit()
    db.refresh(new_route)

    return {
        "message": "Route created successfully",
        "route_id": new_route.id,
        "source": source.name,
        "destination": destination.name,
        "distance": distance
    }


@router.get("/shortest-path")
def shortest_path(
    start_location_id: int,
    end_location_id: int,
    db: Session = Depends(get_db)
):

    routes = db.query(Route).all()

    graph = Graph()

    for route in routes:
        graph.add_edge(
            route.source_location_id,
            route.destination_location_id,
            route.distance
        )

    if start_location_id not in graph.graph:
        raise HTTPException(
            status_code=404,
            detail="Start location is not connected to any route"
        )

    if end_location_id not in graph.graph:
        raise HTTPException(
            status_code=404,
            detail="End location is not connected to any route"
        )

    result = graph.dijkstra(
        start_location_id,
        end_location_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No route found between the locations"
        )

    path_names = []

    for location_id in result["path"]:

        location = db.query(Location).filter(
            Location.id == location_id
        ).first()

        if location:
            path_names.append(location.name)

    return {
        "distance": result["distance"],
        "path": result["path"],
        "path_names": path_names
    }