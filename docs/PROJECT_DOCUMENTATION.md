# Smart Emergency Response and Resource Allocation System
## Detailed Project Documentation

---

## 1. Introduction

### 1.1 Project Title

**Smart Emergency Response and Resource Allocation System**

### 1.2 Project Type

Academic software prototype and decision-support simulation.

### 1.3 Purpose

The system is designed to demonstrate how classical data structures, algorithms, database concepts, REST APIs, and software architecture can be combined to build a practical emergency response management application.

The application allows emergency requests to be registered and monitored, prioritizes emergencies according to severity, identifies suitable response resources, calculates shortest routes, creates dispatch assignments, and tracks the dispatch lifecycle.

The system is intentionally implemented as a prototype. It does not connect to real emergency-service infrastructure and should not be used for actual emergency operations.

---

# 2. Problem Definition

Emergency management may involve multiple incidents occurring simultaneously while response resources are limited and distributed across different locations.

A software system supporting this process should provide mechanisms for:

- recording emergency requests,
- determining which request requires attention first,
- identifying the type of resource needed,
- finding available resources,
- calculating an efficient route,
- assigning a resource,
- monitoring dispatch progress, and
- maintaining persistent records.

The project models these requirements using a web-based application backed by a relational database.

---

# 3. Objectives

The project objectives are:

1. Develop a centralized emergency response dashboard.
2. Store emergency and resource information in a structured database.
3. Prioritize emergencies according to severity.
4. Implement a priority queue using a min-heap.
5. Model locations and routes as a weighted graph.
6. Implement Dijkstra's shortest-path algorithm.
7. Match emergency types to suitable resource types.
8. Select the nearest available suitable resource.
9. Create and track dispatch records.
10. Provide REST APIs for system operations.
11. Test the core algorithms automatically.
12. Demonstrate practical application of data structures, algorithms, databases, and software engineering principles.

---

# 4. Scope

## 4.1 Included in the Current Prototype

- Emergency creation and listing.
- Location management.
- Response resource management.
- Route management.
- Emergency prioritization.
- Shortest route calculation.
- Resource allocation.
- Dispatch creation.
- Dispatch status tracking.
- Dashboard statistics and analytics.
- SQLite persistence.
- REST API access.
- Swagger/OpenAPI documentation.
- Automated algorithm tests.

## 4.2 Outside the Current Scope

- Real emergency dispatch integration.
- Live GPS hardware.
- Real-time road traffic data.
- Direct police/fire/medical service integration.
- Production-grade authentication.
- Guaranteed real-world ETA.
- Autonomous emergency decision making.
- Cloud-scale deployment.

---

# 5. Functional Requirements

## FR1 — Emergency Management

The system shall allow an emergency request to be created with:

- emergency type,
- severity,
- description,
- location, and
- optional reporting user.

The system shall allow stored emergencies to be retrieved.

## FR2 — Emergency Prioritization

The system shall prioritize emergencies using:

```text
CRITICAL = 1
HIGH     = 2
MEDIUM   = 3
LOW      = 4
```

For equal severity, creation time is used to determine ordering.

## FR3 — Resource Management

The system shall store response resources with:

- name,
- resource type,
- operational status,
- capacity, and
- current location.

## FR4 — Route Management

The system shall store weighted connections between locations.

Each route contains:

- source,
- destination,
- distance.

## FR5 — Shortest Path

The system shall calculate the shortest path between two connected locations using Dijkstra's algorithm.

## FR6 — Resource Allocation

The system shall:

1. determine the resource type required,
2. filter unavailable resources,
3. filter resources of the wrong type,
4. calculate route distances, and
5. select the nearest suitable resource.

## FR7 — Dispatch

The system shall create a dispatch connecting an emergency with a resource.

## FR8 — Dispatch Tracking

The system shall support:

```text
DISPATCHED
EN_ROUTE
ARRIVED
RESOLVED
```

and update related emergency/resource states.

## FR9 — Dashboard

The system shall display operational information through a browser-based dashboard.

---

# 6. Non-Functional Requirements

## 6.1 Usability

The dashboard should present emergency, resource, dispatch, and analytics information in a clear format.

## 6.2 Maintainability

The application separates:

- database configuration,
- models,
- schemas,
- routes,
- algorithms,
- templates, and
- static frontend assets.

## 6.3 Testability

Core algorithms are isolated into Python modules and tested using Pytest.

## 6.4 Portability

The project can run in a Python virtual environment on a compatible operating system.

## 6.5 Performance

The current prototype is intended for academic/local use. It is not benchmarked or optimized for production-scale emergency workloads.

---

# 7. Technology Architecture

## 7.1 Technology Layers

### Presentation Layer

- HTML
- CSS
- JavaScript

### Application/API Layer

- FastAPI

### Business/Algorithm Layer

- Priority Queue
- Dijkstra Graph
- Resource Allocation
- Dispatch Lifecycle Logic

### Data Access Layer

- SQLAlchemy ORM

### Persistence Layer

- SQLite

---

# 8. High-Level Architecture

```text
                     ┌───────────────────────┐
                     │       Browser         │
                     │ HTML/CSS/JavaScript   │
                     └───────────┬───────────┘
                                 │
                            HTTP/REST
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │       FastAPI         │
                     │      API Routes       │
                     └───────────┬───────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       Priority Queue       Graph/Dijkstra   Resource Allocation
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 ▼
                     ┌───────────────────────┐
                     │     SQLAlchemy ORM    │
                     └───────────┬───────────┘
                                 ▼
                     ┌───────────────────────┐
                     │   SQLite Database     │
                     └───────────────────────┘
```

---

# 9. Application Workflow

```text
User
 │
 ▼
Dashboard
 │
 ▼
Create Emergency
 │
 ▼
Emergency stored in database
 │
 ▼
Priority Queue
 │
 ▼
Emergency type determines required resource
 │
 ▼
Available resources filtered
 │
 ▼
Dijkstra calculates route distances
 │
 ▼
Nearest suitable resource selected
 │
 ▼
Dispatch created
 │
 ▼
DISPATCHED
 │
 ▼
EN_ROUTE
 │
 ▼
ARRIVED
 │
 ▼
RESOLVED
```

---

# 10. Module Design

## 10.1 `app/main.py`

Responsibilities:

- initialize FastAPI,
- create database tables,
- configure static files,
- configure templates,
- register API routers,
- serve the dashboard.

---

## 10.2 Database Module

### `app/database/database.py`

Responsibilities:

- configure SQLite connection,
- create SQLAlchemy engine,
- create session factory,
- expose declarative base.

The database URL is:

```text
sqlite:///./emergency_response.db
```

### `app/database/session.py`

Provides the database dependency used by FastAPI routes.

The dependency creates a session and closes it after the request.

---

# 11. Data Model

## 11.1 User

Main attributes:

```text
id
name
email
password
role
```

A user may report emergency requests.

## 11.2 Location

Main attributes:

```text
id
name
latitude
longitude
```

A location is used as the node of the route graph.

## 11.3 Resource

Main attributes:

```text
id
name
type
status
capacity
location_id
```

`location_id` identifies the resource's current location.

## 11.4 Emergency

Main attributes:

```text
id
type
severity
description
status
location_id
reported_by
created_at
```

## 11.5 Route

Main attributes:

```text
id
source_location_id
destination_location_id
distance
```

A route represents a weighted graph edge.

## 11.6 Dispatch

Main attributes:

```text
id
emergency_id
resource_id
distance
estimated_time
status
dispatched_at
arrived_at
resolved_at
```

---

# 12. Database Relationships

Conceptual relationship structure:

```text
USER
 │
 │ reports
 ▼
EMERGENCY
 │
 │ assigned through
 ▼
DISPATCH
 │
 │ uses
 ▼
RESOURCE
 │
 │ located at
 ▼
LOCATION

LOCATION ───── ROUTE ───── LOCATION
```

More specifically:

- `Emergency.location_id` references `Location.id`.
- `Emergency.reported_by` references `User.id` when provided.
- `Resource.location_id` references `Location.id`.
- `Route.source_location_id` references `Location.id`.
- `Route.destination_location_id` references `Location.id`.
- `Dispatch.emergency_id` references `Emergency.id`.
- `Dispatch.resource_id` references `Resource.id`.

---

# 13. Emergency Priority Queue

## 13.1 Purpose

When multiple emergencies exist, the system needs a deterministic ordering mechanism.

A priority queue is appropriate because the next highest-priority emergency can be retrieved without sorting the complete collection after every insertion.

## 13.2 Implementation

The project uses Python's `heapq`.

The queue stores:

```text
(priority, created_at, emergency_id, emergency)
```

Example:

```text
(1, 10:00, 5, Emergency 5)
(2, 09:55, 3, Emergency 3)
(4, 09:40, 7, Emergency 7)
```

Emergency 5 is processed before the lower-priority emergencies.

## 13.3 Complexity

For `n` queued emergencies:

- insertion: O(log n)
- removal of next emergency: O(log n)
- empty check: O(1)
- size check: O(1)

---

# 14. Dijkstra's Shortest Path

## 14.1 Purpose

The route network is represented as a weighted graph.

For example:

```text
Main Hospital
     |
    2 km
     |
Fire Station
     |
    3 km
     |
Police Station
     |
    2 km
     |
City Center
```

The graph can also contain alternative routes.

## 14.2 Algorithm Steps

1. Initialize all distances to infinity.
2. Set the source distance to zero.
3. Insert the source into a min-priority queue.
4. Select the node with the smallest current distance.
5. Examine neighboring nodes.
6. Calculate alternative distances.
7. Update a neighbor when a shorter route is found.
8. Repeat until the destination is reached or all reachable nodes are processed.
9. Reconstruct the route using predecessor information.

## 14.3 Example

For:

```text
1 → 2 = 2 km
2 → 3 = 3 km
3 → 4 = 2 km
1 → 4 = 6 km
```

The shortest path from location 1 to location 3 is:

```text
1 → 2 → 3
```

with distance:

```text
2 + 3 = 5 km
```

The shortest path from 1 to 4 is the direct 6 km route because:

```text
1 → 2 → 3 → 4
= 2 + 3 + 2
= 7 km
```

while:

```text
1 → 4
= 6 km
```

## 14.4 Complexity

Using a binary heap:

```text
O((V + E) log V)
```

where:

- `V` = number of vertices,
- `E` = number of edges.

---

# 15. Resource Allocation

## 15.1 Resource Mapping

The prototype uses the following mapping:

```text
MEDICAL    → AMBULANCE
FIRE       → FIRE_TRUCK
ACCIDENT   → AMBULANCE
SECURITY   → POLICE_VEHICLE
OTHER      → RESCUE_TEAM
```

## 15.2 Allocation Process

```text
Emergency
    ↓
Identify required resource type
    ↓
Find resources with matching type
    ↓
Remove unavailable resources
    ↓
Calculate route to emergency
    ↓
Compare distances
    ↓
Select nearest resource
```

## 15.3 Important Rule

A resource is considered only when:

```text
resource.status == "AVAILABLE"
```

This prevents already busy or dispatched resources from being selected again.

---

# 16. Estimated Response Time

For the prototype dispatch calculation, estimated time is derived from route distance using a simplified assumed speed:

```text
ETA (minutes) = (distance / 30) × 60
```

This represents an illustrative average speed of 30 km/h.

This is **not a real traffic-aware ETA** and should not be interpreted as a production emergency-response prediction.

---

# 17. Dispatch Lifecycle

A dispatch follows:

```text
DISPATCHED
     ↓
 EN_ROUTE
     ↓
  ARRIVED
     ↓
 RESOLVED
```

### DISPATCHED

- Emergency becomes assigned.
- Resource becomes dispatched.

### EN_ROUTE

- Emergency becomes en route.
- Resource becomes busy.

### ARRIVED

- Emergency becomes in progress.
- Arrival timestamp is recorded.

### RESOLVED

- Emergency becomes resolved.
- Resource becomes available.
- Resolution timestamp is recorded.

---

# 18. REST API Design

## 18.1 Location APIs

### Create Location

```http
POST /locations/
```

Example request:

```json
{
  "name": "Main Hospital",
  "latitude": 12.9716,
  "longitude": 77.5946
}
```

### List Locations

```http
GET /locations/
```

---

# 19. Resource APIs

### Create Resource

```http
POST /resources/
```

Example:

```json
{
  "name": "Ambulance 1",
  "type": "AMBULANCE",
  "capacity": 1,
  "location_id": 1
}
```

### List Resources

```http
GET /resources/
```

---

# 20. Emergency APIs

### Create Emergency

```http
POST /emergencies/
```

Example:

```json
{
  "type": "MEDICAL",
  "severity": "CRITICAL",
  "description": "Medical emergency",
  "location_id": 4
}
```

### List Emergencies

```http
GET /emergencies/
```

---

# 21. Priority API

```http
GET /priority/emergencies
```

Returns emergency requests ordered using the priority queue logic.

The dashboard converts severity into the displayed priority values.

---

# 22. Route APIs

### Create Route

```http
POST /routes/
```

Example:

```json
{
  "source_location_id": 1,
  "destination_location_id": 2,
  "distance": 2
}
```

### Shortest Path

```http
GET /routes/shortest-path
```

The endpoint uses the graph implementation and Dijkstra's algorithm.

---

# 23. Dispatch APIs

### Assign Resource

```http
POST /dispatches/assign/{emergency_id}
```

The endpoint:

1. retrieves the emergency,
2. retrieves available resources,
3. retrieves routes,
4. invokes the resource allocator,
5. calculates the selected route,
6. creates the dispatch,
7. updates emergency/resource status,
8. returns dispatch information.

### List Dispatches

```http
GET /dispatches/
```

The response includes information such as:

- emergency,
- resource,
- source location,
- destination location,
- route,
- route distance,
- estimated time,
- dispatch status.

---

# 24. Dispatch Tracking API

```http
PUT /dispatches/{dispatch_id}/status
```

Supported statuses:

```text
DISPATCHED
EN_ROUTE
ARRIVED
RESOLVED
```

The endpoint validates the status and updates the associated emergency and resource.

---

# 25. Frontend Design

The dashboard is implemented using:

- HTML for structure,
- CSS for presentation,
- JavaScript for API interaction.

The dashboard is served through FastAPI using Jinja2 templates and static files.

Main sections include:

1. Header
2. Statistics cards
3. Create Emergency form
4. Emergency Requests
5. Response Resources
6. Active Dispatches
7. System Analytics
8. Emergency Priority Queue
9. Footer

JavaScript retrieves backend data using `fetch()` and updates the interface dynamically.

---

# 26. Dashboard Data Flow

```text
Dashboard loaded
       ↓
Load locations
       ↓
Load emergencies
       ↓
Load resources
       ↓
Load dispatches
       ↓
Load priority queue
       ↓
Calculate/display analytics
```

When an emergency is created:

```text
Form submission
      ↓
POST /emergencies/
      ↓
Database insert
      ↓
Refresh dashboard
```

When a dispatch is assigned:

```text
Dispatch button
      ↓
POST /dispatches/assign/{id}
      ↓
Resource allocation
      ↓
Dijkstra route
      ↓
Dispatch created
      ↓
Dashboard refresh
```

---

# 27. Testing Strategy

Testing focuses on the algorithmic core because these components directly affect prioritization, routing, and allocation behavior.

The project uses:

```text
pytest
```

## 27.1 Priority Queue Tests

Five cases are tested:

1. Critical emergency has priority.
2. Severity ordering is correct.
3. Earlier emergency wins for the same severity.
4. Empty queue returns no emergency.
5. Queue size is maintained.

## 27.2 Dijkstra Tests

Four cases are tested:

1. Shortest path through an intermediate node.
2. Direct route selection.
3. Unreachable destination.
4. Same source and destination.

## 27.3 Resource Allocation Tests

Three cases are tested:

1. Correct resource type is selected.
2. Nearest suitable resource is selected.
3. Unavailable resources are ignored.

## 27.4 Verified Test Result

```text
12 passed
0 warnings
```

This result was obtained after updating deprecated UTC timestamp usage to timezone-aware timestamps.

---

# 28. Error Handling

The FastAPI routes use HTTP exceptions for invalid conditions such as:

- resource/emergency not found,
- dispatch not found,
- related records missing,
- invalid dispatch status,
- no suitable resource available.

This allows the API to return meaningful HTTP error responses instead of silently failing.

---

# 29. Security Considerations

The current prototype has limited security features because it is intended for academic use.

The project should not be deployed directly as a production emergency platform without additional security controls.

Future security improvements should include:

- password hashing,
- secure authentication,
- role-based authorization,
- HTTPS,
- input validation,
- audit logging,
- secret management,
- rate limiting,
- secure database configuration,
- session/token security.

---

# 30. System Design Principles

The project follows a separation-of-concerns approach.

Responsibilities are divided into:

```text
Models       → database entities
Schemas      → request/response validation
Routes       → API endpoints
Algorithms   → reusable decision logic
Database     → persistence
Templates    → page structure
Static files → frontend styling and behavior
Tests        → algorithm verification
```

This makes individual components easier to test and maintain.

---

# 31. Complexity Summary

| Operation | Complexity |
|---|---|
| Priority Queue insertion | O(log n) |
| Priority Queue removal | O(log n) |
| Priority Queue size | O(1) |
| Dijkstra with heap | O((V + E) log V) |
| Candidate resource sorting | O(R log R) |
| Database lookup | Depends on query/indexing |

Where:

- `n` = number of queued emergencies,
- `V` = graph vertices,
- `E` = graph edges,
- `R` = number of candidate resources.

The prototype does not claim production-scale performance.

---

# 32. Example End-to-End Scenario

Consider the following locations:

```text
1. Main Hospital
2. Fire Station
3. Police Station
4. City Center
```

Routes:

```text
1 ↔ 2 = 2 km
2 ↔ 3 = 3 km
3 ↔ 4 = 2 km
1 ↔ 4 = 6 km
```

Suppose a medical emergency occurs at City Center.

The system:

1. Stores the emergency.
2. Classifies it as `MEDICAL`.
3. Maps `MEDICAL` to `AMBULANCE`.
4. Finds available ambulances.
5. Calculates routes to City Center.
6. Selects the ambulance with the shortest route.
7. Creates a dispatch.
8. Calculates prototype ETA.
9. Displays the dispatch on the dashboard.
10. Allows the dispatch status to progress through the lifecycle.

This demonstrates how the data structure and algorithm components cooperate with the database and web interface.

---

# 33. Setup Instructions

## Prerequisites

Install:

- Python 3.12+
- pip

## Create environment

```bat
python -m venv venv
```

## Activate environment

```bat
venv\Scripts\activate
```

## Install dependencies

```bat
pip install -r requirements.txt
```

## Start server

```bat
uvicorn app.main:app --reload
```

## Open application

```text
http://127.0.0.1:8000/
```

## Open API documentation

```text
http://127.0.0.1:8000/docs
```

## Run tests

```bat
pytest -v
```

---

# 34. Configuration and Runtime Notes

The project currently uses SQLite with:

```text
sqlite:///./emergency_response.db
```

FastAPI creates the database tables through SQLAlchemy during application startup.

For local development, the database is stored in the project directory.

The virtual environment should not be committed to source control.

---

# 35. GitHub Packaging

Recommended repository contents:

```text
app/
tests/
docs/
README.md
requirements.txt
pytest.ini
.gitignore
```

Do not commit:

```text
venv/
__pycache__/
.pytest_cache/
*.db
.env
.idea/
.vscode/
```

---

# 36. Limitations and Assumptions

The project makes several simplifications for the academic prototype:

1. Locations are represented by database records.
2. Route distances are manually stored.
3. The route graph uses non-negative distances.
4. Resource locations are database values rather than live GPS positions.
5. ETA uses a simplified assumed speed.
6. Emergency classification is rule-based.
7. No machine-learning model is used in the current version.
8. No real-time external emergency communication is implemented.
9. Authentication is not the focus of the current prototype.
10. The system is not designed for production emergency workloads.

These limitations are intentional and make the project feasible as an academic software prototype.

---

# 37. Future Enhancements

## 37.1 Live Maps

Integrate a mapping provider to visualize:

- resource location,
- emergency location,
- shortest route.

## 37.2 Traffic-Aware Routing

Use real-time traffic information to make route selection more realistic.

## 37.3 GPS Tracking

Allow resources to transmit their live location.

## 37.4 WebSockets

Replace periodic dashboard refreshes with real-time server-to-browser updates.

## 37.5 Notifications

Add SMS, email, or push notifications.

## 37.6 Authentication

Implement secure login and role-based access.

## 37.7 Historical Analytics

Store response history and calculate:

- average response time,
- resource utilization,
- emergency frequency,
- location-based incident statistics.

## 37.8 Predictive Analytics

Historical data could later be used for predictive analysis. This would be a separate extension and is not part of the current algorithmic implementation.

## 37.9 Cloud Deployment

The application could later be deployed using a cloud-hosted database and application server.

---

# 38. Academic Relevance

The project demonstrates practical use of multiple software development and computer science concepts.

### Python and OOP

The project uses Python classes for reusable algorithmic components such as the priority queue and graph.

### Data Structures

The project demonstrates:

- heaps,
- priority queues,
- graphs,
- dictionaries,
- lists.

### Algorithms

The project demonstrates:

- priority scheduling,
- Dijkstra shortest path,
- candidate selection,
- sorting.

### Databases

The project demonstrates:

- entities,
- primary keys,
- foreign keys,
- CRUD operations,
- relational data,
- ORM-based persistence.

### System Design

The project demonstrates:

- layered architecture,
- separation of concerns,
- API design,
- modular components.

### Testing

Pytest is used to verify algorithm behavior through automated test cases.

---

# 39. Conclusion

The Smart Emergency Response and Resource Allocation System demonstrates how fundamental computer science concepts can be combined into a practical software application.

The central workflow is:

```text
Prioritize Emergency
        ↓
Identify Required Resource
        ↓
Find Available Candidates
        ↓
Calculate Shortest Routes
        ↓
Select Nearest Suitable Resource
        ↓
Create Dispatch
        ↓
Track Response
```

The current implementation successfully demonstrates the core algorithmic and software-engineering requirements of the prototype, with all 12 automated algorithm tests passing and zero warnings in the verified test run.

The system is intentionally scoped as an academic decision-support prototype. Future versions could integrate live maps, GPS, traffic data, real-time communication, stronger security, cloud infrastructure, and historical/predictive analytics.
