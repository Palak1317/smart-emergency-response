from app.algorithms.graph import Graph


RESOURCE_REQUIREMENTS = {
    "MEDICAL": "AMBULANCE",
    "FIRE": "FIRE_TRUCK",
    "ACCIDENT": "AMBULANCE",
    "SECURITY": "POLICE_VEHICLE",
    "OTHER": "RESCUE_TEAM"
}


def get_required_resource_type(emergency_type):
    return RESOURCE_REQUIREMENTS.get(
        emergency_type.upper(),
        "RESCUE_TEAM"
    )


def find_best_resource(
    emergency,
    resources,
    routes
):
    required_type = get_required_resource_type(
        emergency.type
    )

    graph = Graph()

    for route in routes:
        graph.add_edge(
            route.source_location_id,
            route.destination_location_id,
            route.distance
        )

    candidates = []

    for resource in resources:

        if resource.status != "AVAILABLE":
            continue

        if resource.type.upper() != required_type:
            continue

        result = graph.dijkstra(
            resource.location_id,
            emergency.location_id
        )

        if result is None:
            continue

        candidates.append({
            "resource": resource,
            "distance": result["distance"],
            "path": result["path"]
        })

    if not candidates:
        return None

    candidates.sort(
        key=lambda candidate: candidate["distance"]
    )

    return candidates[0]