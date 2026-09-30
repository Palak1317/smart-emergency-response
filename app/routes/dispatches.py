from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.emergency import Emergency
from app.models.resource import Resource
from app.models.route import Route
from app.models.dispatch import Dispatch
from app.models.location import Location

from app.algorithms.resource_allocator import find_best_resource
from app.algorithms.graph import Graph


router = APIRouter(
    prefix="/dispatches",
    tags=["Dispatch"]
)


# =========================================================
# ASSIGN RESOURCE TO EMERGENCY
# =========================================================

@router.post("/assign/{emergency_id}")
def assign_resource(
    emergency_id: int,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Find emergency
    # -----------------------------------------------------

    emergency = (
        db.query(Emergency)
        .filter(Emergency.id == emergency_id)
        .first()
    )

    if not emergency:
        raise HTTPException(
            status_code=404,
            detail="Emergency not found"
        )


    # -----------------------------------------------------
    # Emergency must be pending
    # -----------------------------------------------------

    if emergency.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Emergency is not pending"
        )


    # -----------------------------------------------------
    # Get available resources
    # -----------------------------------------------------

    resources = (
        db.query(Resource)
        .filter(Resource.status == "AVAILABLE")
        .all()
    )

    if not resources:
        raise HTTPException(
            status_code=404,
            detail="No available resources"
        )


    # -----------------------------------------------------
    # Get all routes
    # -----------------------------------------------------

    routes = db.query(Route).all()


    # -----------------------------------------------------
    # Find best resource using:
    #
    # 1. Emergency type
    # 2. Resource type
    # 3. Dijkstra shortest path
    # -----------------------------------------------------

    result = find_best_resource(
        emergency,
        resources,
        routes
    )


    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No suitable resource found"
        )


    resource = result["resource"]

    distance = result["distance"]

    path = result["path"]


    # -----------------------------------------------------
    # Calculate estimated travel time
    #
    # Prototype assumption:
    # Average speed = 30 km/h
    # -----------------------------------------------------

    estimated_time = (distance / 30) * 60


    # -----------------------------------------------------
    # Create dispatch
    # -----------------------------------------------------

    dispatch = Dispatch(

        emergency_id=emergency.id,

        resource_id=resource.id,

        distance=distance,

        estimated_time=estimated_time,

        status="DISPATCHED",

        dispatched_at=datetime.now(timezone.utc)

    )


    db.add(dispatch)


    # -----------------------------------------------------
    # Update emergency and resource
    # -----------------------------------------------------

    emergency.status = "ASSIGNED"

    resource.status = "DISPATCHED"


    db.commit()

    db.refresh(dispatch)


    # -----------------------------------------------------
    # Convert location IDs to location names
    # -----------------------------------------------------

    route_names = []

    for location_id in path:

        location = (
            db.query(Location)
            .filter(Location.id == location_id)
            .first()
        )

        if location:
            route_names.append(location.name)


    # -----------------------------------------------------
    # Return dispatch information
    # -----------------------------------------------------

    return {

        "message":
            "Resource assigned successfully",

        "emergency_id":
            emergency.id,

        "resource_id":
            resource.id,

        "resource_name":
            resource.name,

        "resource_type":
            resource.type,

        "distance":
            distance,

        "estimated_time_minutes":
            round(estimated_time, 2),

        "route":
            path,

        "route_names":
            route_names,

        "status":
            dispatch.status

    }


# =========================================================
# GET ALL DISPATCHES
# =========================================================

@router.get("/")
def get_dispatches(
    db: Session = Depends(get_db)
):

    dispatches = (
        db.query(Dispatch)
        .order_by(Dispatch.id.desc())
        .all()
    )


    result = []


    for dispatch in dispatches:

        # -------------------------------------------------
        # Get emergency
        # -------------------------------------------------

        emergency = (
            db.query(Emergency)
            .filter(
                Emergency.id ==
                dispatch.emergency_id
            )
            .first()
        )


        # -------------------------------------------------
        # Get resource
        # -------------------------------------------------

        resource = (
            db.query(Resource)
            .filter(
                Resource.id ==
                dispatch.resource_id
            )
            .first()
        )


        # -------------------------------------------------
        # Get source location
        #
        # Resource's current location
        # -------------------------------------------------

        source_location = None

        if resource:

            source_location = (
                db.query(Location)
                .filter(
                    Location.id ==
                    resource.location_id
                )
                .first()
            )


        # -------------------------------------------------
        # Get destination location
        #
        # Emergency location
        # -------------------------------------------------

        destination_location = None

        if emergency:

            destination_location = (
                db.query(Location)
                .filter(
                    Location.id ==
                    emergency.location_id
                )
                .first()
            )


        # -------------------------------------------------
        # Calculate shortest path again
        #
        # This allows the dashboard to display
        # the actual Dijkstra route.
        # -------------------------------------------------

        route_path = []

        route_names = []

        route_distance = dispatch.distance


        if resource and emergency:

            routes = db.query(Route).all()

            graph = Graph()


            for route in routes:

                graph.add_edge(

                    route.source_location_id,

                    route.destination_location_id,

                    route.distance

                )


            shortest_path = graph.dijkstra(

                resource.location_id,

                emergency.location_id

            )


            if shortest_path:

                route_path = shortest_path["path"]

                route_distance = shortest_path["distance"]


                # -----------------------------------------
                # Convert path IDs to location names
                # -----------------------------------------

                for location_id in route_path:

                    location = (
                        db.query(Location)
                        .filter(
                            Location.id ==
                            location_id
                        )
                        .first()
                    )

                    if location:
                        route_names.append(
                            location.name
                        )


        # -------------------------------------------------
        # Route text
        # -------------------------------------------------

        if route_names:

            route_text = " → ".join(
                route_names
            )

        elif (
            source_location and
            destination_location
        ):

            route_text = (
                f"{source_location.name} "
                f"→ "
                f"{destination_location.name}"
            )

        else:

            route_text = "Route unavailable"


        # -------------------------------------------------
        # Emergency information
        # -------------------------------------------------

        emergency_type = None
        emergency_severity = None

        if emergency:

            emergency_type = emergency.type

            emergency_severity = emergency.severity


        # -------------------------------------------------
        # Resource information
        # -------------------------------------------------

        resource_name = None
        resource_type = None

        if resource:

            resource_name = resource.name

            resource_type = resource.type


        # -------------------------------------------------
        # Add dispatch to result
        # -------------------------------------------------

        result.append({

            "id":
                dispatch.id,

            "emergency_id":
                dispatch.emergency_id,

            "emergency_type":
                emergency_type,

            "emergency_severity":
                emergency_severity,

            "resource_id":
                dispatch.resource_id,

            "resource_name":
                resource_name,

            "resource_type":
                resource_type,

            "source_location_name":
                source_location.name
                if source_location
                else None,

            "destination_location_name":
                destination_location.name
                if destination_location
                else None,

            "route":
                route_text,

            "route_path":
                route_path,

            "route_names":
                route_names,

            "distance":
                route_distance,

            "estimated_time_minutes":
                round(
                    dispatch.estimated_time,
                    2
                )
                if dispatch.estimated_time
                is not None
                else None,

            "status":
                dispatch.status,

            "dispatched_at":
                dispatch.dispatched_at,

            "arrived_at":
                dispatch.arrived_at,

            "resolved_at":
                dispatch.resolved_at

        })


    return result