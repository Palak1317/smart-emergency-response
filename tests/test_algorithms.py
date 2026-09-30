from datetime import datetime, timedelta, timezone

from app.algorithms.priority_queue import EmergencyPriorityQueue
from app.algorithms.graph import Graph
from app.algorithms.resource_allocator import find_best_resource


# ============================================================
# MOCK CLASSES
# ============================================================

class MockEmergency:

    def __init__(
        self,
        emergency_id,
        severity,
        created_at,
        emergency_type="MEDICAL",
        location_id=1
    ):
        self.id = emergency_id
        self.severity = severity
        self.created_at = created_at
        self.type = emergency_type
        self.location_id = location_id


class MockResource:

    def __init__(
        self,
        resource_id,
        resource_type,
        location_id,
        status="AVAILABLE"
    ):
        self.id = resource_id
        self.type = resource_type
        self.location_id = location_id
        self.status = status


class MockRoute:

    def __init__(
        self,
        source_location_id,
        destination_location_id,
        distance
    ):
        self.source_location_id = source_location_id
        self.destination_location_id = destination_location_id
        self.distance = distance


# ============================================================
# PRIORITY QUEUE TESTS
# ============================================================

def test_critical_emergency_has_priority():

    queue = EmergencyPriorityQueue()

    now = datetime.now(timezone.utc)

    low = MockEmergency(
        1,
        "LOW",
        now
    )

    critical = MockEmergency(
        2,
        "CRITICAL",
        now + timedelta(minutes=1)
    )

    queue.add_emergency(low)
    queue.add_emergency(critical)

    next_emergency = queue.get_next_emergency()

    assert next_emergency.id == 2
    assert next_emergency.severity == "CRITICAL"


def test_priority_order():

    queue = EmergencyPriorityQueue()

    now = datetime.now(timezone.utc)

    low = MockEmergency(
        1,
        "LOW",
        now
    )

    medium = MockEmergency(
        2,
        "MEDIUM",
        now
    )

    high = MockEmergency(
        3,
        "HIGH",
        now
    )

    critical = MockEmergency(
        4,
        "CRITICAL",
        now
    )

    queue.add_emergency(low)
    queue.add_emergency(medium)
    queue.add_emergency(high)
    queue.add_emergency(critical)

    assert queue.get_next_emergency().severity == "CRITICAL"
    assert queue.get_next_emergency().severity == "HIGH"
    assert queue.get_next_emergency().severity == "MEDIUM"
    assert queue.get_next_emergency().severity == "LOW"


def test_same_priority_uses_time():

    queue = EmergencyPriorityQueue()

    now = datetime.now(timezone.utc)

    earlier = MockEmergency(
        1,
        "CRITICAL",
        now
    )

    later = MockEmergency(
        2,
        "CRITICAL",
        now + timedelta(minutes=5)
    )

    queue.add_emergency(later)
    queue.add_emergency(earlier)

    next_emergency = queue.get_next_emergency()

    assert next_emergency.id == 1


def test_empty_queue():

    queue = EmergencyPriorityQueue()

    assert queue.is_empty() is True
    assert queue.size() == 0
    assert queue.get_next_emergency() is None


def test_queue_size():

    queue = EmergencyPriorityQueue()

    now = datetime.now(timezone.utc)

    emergency1 = MockEmergency(
        1,
        "HIGH",
        now
    )

    emergency2 = MockEmergency(
        2,
        "LOW",
        now
    )

    queue.add_emergency(emergency1)
    queue.add_emergency(emergency2)

    assert queue.size() == 2

    queue.get_next_emergency()

    assert queue.size() == 1


# ============================================================
# DIJKSTRA TESTS
# ============================================================

def test_dijkstra_shortest_path():

    graph = Graph()

    graph.add_edge(1, 2, 2)
    graph.add_edge(2, 3, 3)
    graph.add_edge(3, 4, 2)
    graph.add_edge(1, 4, 6)

    result = graph.dijkstra(1, 3)

    assert result is not None
    assert result["distance"] == 5
    assert result["path"] == [1, 2, 3]


def test_dijkstra_direct_route():

    graph = Graph()

    graph.add_edge(1, 2, 2)
    graph.add_edge(2, 3, 3)
    graph.add_edge(3, 4, 2)
    graph.add_edge(1, 4, 6)

    result = graph.dijkstra(1, 4)

    assert result is not None
    assert result["distance"] == 6
    assert result["path"] == [1, 4]


def test_dijkstra_unreachable_node():

    graph = Graph()

    graph.add_edge(1, 2, 5)
    graph.add_edge(3, 4, 5)

    result = graph.dijkstra(1, 4)

    assert result is None


def test_dijkstra_same_source_destination():

    graph = Graph()

    graph.add_edge(1, 2, 5)

    result = graph.dijkstra(1, 1)

    assert result is not None
    assert result["distance"] == 0
    assert result["path"] == [1]


# ============================================================
# RESOURCE ALLOCATION TESTS
# ============================================================

def test_resource_allocation_correct_resource_type():

    emergency = MockEmergency(
        1,
        "CRITICAL",
        datetime.now(timezone.utc),
        emergency_type="MEDICAL",
        location_id=2
    )

    ambulance = MockResource(
        1,
        "AMBULANCE",
        location_id=1
    )

    fire_truck = MockResource(
        2,
        "FIRE_TRUCK",
        location_id=1
    )

    routes = [
        MockRoute(1, 2, 5)
    ]

    result = find_best_resource(
        emergency,
        [ambulance, fire_truck],
        routes
    )

    assert result is not None
    assert result["resource"].id == 1


def test_resource_allocation_nearest_resource():

    emergency = MockEmergency(
        1,
        "HIGH",
        datetime.now(timezone.utc),
        emergency_type="MEDICAL",
        location_id=3
    )

    ambulance1 = MockResource(
        1,
        "AMBULANCE",
        location_id=1
    )

    ambulance2 = MockResource(
        2,
        "AMBULANCE",
        location_id=2
    )

    routes = [
        MockRoute(1, 2, 10),
        MockRoute(2, 3, 2),
        MockRoute(1, 3, 20)
    ]

    result = find_best_resource(
        emergency,
        [ambulance1, ambulance2],
        routes
    )

    assert result is not None
    assert result["resource"].id == 2
    assert result["distance"] == 2


def test_unavailable_resource_is_ignored():

    emergency = MockEmergency(
        1,
        "CRITICAL",
        datetime.now(timezone.utc),
        emergency_type="MEDICAL",
        location_id=2
    )

    unavailable_ambulance = MockResource(
        1,
        "AMBULANCE",
        location_id=1,
        status="BUSY"
    )

    available_ambulance = MockResource(
        2,
        "AMBULANCE",
        location_id=1,
        status="AVAILABLE"
    )

    routes = [
        MockRoute(1, 2, 5)
    ]

    result = find_best_resource(
        emergency,
        [unavailable_ambulance, available_ambulance],
        routes
    )

    assert result is not None
    assert result["resource"].id == 2