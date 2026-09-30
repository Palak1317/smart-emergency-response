# Smart Emergency Response and Resource Allocation System

A web-based emergency response decision-support prototype that prioritizes emergency requests, finds shortest routes between locations, allocates suitable available response resources, and tracks dispatch status through a centralized dashboard.

> **Academic prototype:** This project is designed for academic demonstration and decision support. It is not a replacement for real emergency dispatch, medical, police, fire, or public-safety infrastructure.

---

## 1. Project Overview

During an emergency, multiple requests may arrive while response resources are limited or distributed across different locations. A response system therefore needs to answer three practical questions:

1. Which emergency should be handled first?
2. Which suitable response resource should be assigned?
3. What is the shortest available route between the resource and the emergency?

This project implements these functions as a software prototype using Python, FastAPI, SQLite, SQLAlchemy, and classical data structures and algorithms.

The system uses:

- A **priority queue implemented with a min-heap** for emergency prioritization.
- **Dijkstra's shortest-path algorithm** for route calculation.
- **Resource allocation logic** to select the nearest available resource of the required type.
- A **relational SQLite database** for persistent application data.
- A browser-based dashboard for monitoring and dispatch tracking.
- REST APIs exposed through FastAPI and documented automatically with OpenAPI/Swagger.
- Pytest-based automated tests for the core algorithms.

---

## 2. Problem Statement

Emergency response can become difficult when several incidents are reported at the same time and response resources are limited.

A basic response management system should be able to:

- register emergency requests,
- classify their severity,
- prioritize requests,
- identify suitable resources,
- calculate efficient routes,
- create dispatch assignments,
- track dispatch progress, and
- provide an overview of current system activity.

The proposed system provides these capabilities in a controlled academic prototype.

---

## 3. Objectives

The main objectives are:

- Build a centralized emergency response management dashboard.
- Prioritize emergencies according to severity.
- Use a priority queue to model emergency scheduling.
- Represent locations and roads as a weighted graph.
- Use Dijkstra's algorithm to calculate shortest routes.
- Match emergency types with appropriate resource types.
- Select the nearest available suitable resource.
- Track the lifecycle of a dispatch.
- Store application data using a relational database.
- Expose operations through REST APIs.
- Demonstrate practical use of data structures, algorithms, databases, and software engineering concepts.
- Provide automated tests for the core algorithms.

---

## 4. Key Features

### Emergency Management

- Create emergency requests.
- Store emergency type, severity, description, and location.
- View all emergency requests.
- Track emergency status.

### Emergency Prioritization

The system assigns numerical priority values:

| Severity | Priority |
|---|---:|
| CRITICAL | 1 |
| HIGH | 2 |
| MEDIUM | 3 |
| LOW | 4 |

A lower number represents higher urgency.

For emergencies with the same severity, earlier creation time is processed first.

### Resource Management

The prototype supports resource types such as:

- `AMBULANCE`
- `FIRE_TRUCK`
- `POLICE_VEHICLE`
- `RESCUE_TEAM`

Resources have operational states including:

- `AVAILABLE`
- `DISPATCHED`
- `BUSY`

### Shortest Route Calculation

Locations and routes are represented as a weighted graph. Dijkstra's algorithm is used to find the shortest path between a resource's location and an emergency location.

### Resource Allocation

The system maps emergency types to required resource types:

| Emergency Type | Required Resource |
|---|---|
| MEDICAL | AMBULANCE |
| FIRE | FIRE_TRUCK |
| ACCIDENT | AMBULANCE |
| SECURITY | POLICE_VEHICLE |
| OTHER | RESCUE_TEAM |

Only available resources of the required type are considered. The nearest suitable resource is selected according to calculated route distance.

### Dispatch Tracking

Dispatches can progress through:

```text
DISPATCHED → EN_ROUTE → ARRIVED → RESOLVED
```

Corresponding emergency and resource states are updated during the lifecycle.

### Dashboard Analytics

The dashboard provides:

- total emergencies,
- critical emergencies,
- pending emergencies,
- available resources,
- active dispatches,
- emergency request table,
- resource table,
- dispatch table,
- priority queue visualization, and
- emergency/resource analytics.

### API Documentation

FastAPI automatically exposes interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## 5. Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python 3.12+ |
| Backend Framework | FastAPI |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| API Documentation | OpenAPI / Swagger UI |
| Testing | Pytest |
| Version Control | Git / GitHub |

No machine-learning model is required for the current implementation. The core decision logic is algorithmic and rule-based.

---

## 6. System Architecture

The system follows a simple layered architecture:

```text
┌──────────────────────────────────────┐
│              Browser                 │
│      HTML + CSS + JavaScript         │
└──────────────────┬───────────────────┘
                   │ REST API
                   ▼
┌──────────────────────────────────────┐
│             FastAPI                  │
│       API / Route Layer               │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│        Business Logic Layer          │
│                                      │
│ Priority Queue                       │
│ Dijkstra Shortest Path               │
│ Resource Allocation                  │
│ Dispatch Tracking                    │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│          SQLAlchemy ORM              │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│          SQLite Database              │
└──────────────────────────────────────┘
```

### Main request flow

```text
Emergency Created
       ↓
Emergency Stored in Database
       ↓
Priority Queue
       ↓
Required Resource Type Identified
       ↓
Available Resources Filtered
       ↓
Dijkstra Route Calculation
       ↓
Nearest Suitable Resource Selected
       ↓
Dispatch Created
       ↓
Dispatch Status Updated
       ↓
Emergency Resolved
```

---

## 7. Project Structure

```text
Smart-Emergency-Response/
│
├── app/
│   ├── main.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── location.py
│   │   ├── resource.py
│   │   ├── emergency.py
│   │   ├── route.py
│   │   └── dispatch.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── location.py
│   │   ├── resource.py
│   │   └── emergency.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── locations.py
│   │   ├── resources.py
│   │   ├── emergencies.py
│   │   ├── priority.py
│   │   ├── routes.py
│   │   ├── dispatches.py
│   │   └── dispatch_tracking.py
│   │
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── priority_queue.py
│   │   ├── graph.py
│   │   └── resource_allocator.py
│   │
│   ├── templates/
│   │   └── dashboard.html
│   │
│   └── static/
│       ├── style.css
│       └── dashboard.js
│
├── tests/
│   └── test_algorithms.py
│
├── docs/
│   └── PROJECT_DOCUMENTATION.md
│
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
└── emergency_response.db
```

> `emergency_response.db` is a local runtime database and should not be committed to GitHub. The project's `.gitignore` excludes `*.db`.

---

## 8. Database Overview

The database contains the following main entities:

### User

Stores user information such as:

- ID
- name
- email
- password
- role

### Location

Represents locations used by emergencies and resources.

Fields include:

- ID
- name
- latitude
- longitude

### Resource

Represents emergency response resources.

Fields include:

- ID
- name
- type
- status
- capacity
- location ID

### Emergency

Represents reported emergency requests.

Fields include:

- ID
- type
- severity
- description
- status
- location ID
- reported-by user ID
- creation timestamp

### Route

Represents a weighted connection between two locations.

Fields include:

- ID
- source location ID
- destination location ID
- distance

### Dispatch

Connects an emergency with a selected resource.

Fields include:

- ID
- emergency ID
- resource ID
- distance
- estimated time
- status
- dispatched timestamp
- arrived timestamp
- resolved timestamp

---

## 9. Core Algorithms

### 9.1 Priority Queue

Python's `heapq` is used to implement a min-heap.

Each emergency is inserted using:

```text
(priority, creation_time, emergency_id, emergency)
```

This provides:

1. severity-based priority,
2. earlier creation time for equal severity, and
3. emergency ID as a deterministic tie-breaker.

The primary queue operations have logarithmic insertion/removal complexity:

- Insert: O(log n)
- Remove minimum: O(log n)
- Peek/remove next emergency: O(log n) in this implementation because the item is popped.

### 9.2 Dijkstra's Algorithm

The road network is modeled as a weighted graph.

For non-negative route distances, Dijkstra's algorithm finds the shortest path.

With a binary heap priority queue, the implementation operates in approximately:

```text
O((V + E) log V)
```

where:

- `V` = number of locations/vertices
- `E` = number of routes/edges

### 9.3 Resource Allocation

The resource allocator:

1. Determines the resource type required by the emergency.
2. Ignores resources that are not `AVAILABLE`.
3. Ignores resources of the wrong type.
4. Calculates a shortest path from each candidate resource to the emergency.
5. Selects the candidate with minimum distance.

The selected resource is then used to create a dispatch.

---

## 10. API Overview

### Locations

```text
POST /locations/
GET  /locations/
```

### Resources

```text
POST /resources/
GET  /resources/
```

### Emergencies

```text
POST /emergencies/
GET  /emergencies/
```

### Priority Queue

```text
GET /priority/emergencies
```

### Routes

```text
POST /routes/
GET  /routes/shortest-path
```

### Dispatch

```text
POST /dispatches/assign/{emergency_id}
GET  /dispatches/
```

### Dispatch Tracking

```text
PUT /dispatches/{dispatch_id}/status
```

Detailed endpoint behavior is documented in `docs/PROJECT_DOCUMENTATION.md`.

---

## 11. Installation and Setup

### Prerequisites

- Python 3.12 or newer
- pip
- A terminal/command prompt
- A modern web browser

### Create the virtual environment

```bash
python -m venv venv
```

### Activate it on Windows

```bat
venv\Scripts\activate
```

### Install dependencies

```bat
pip install -r requirements.txt
```

### Run the application

```bat
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 12. Running Tests

The project uses Pytest.

Run all tests:

```bat
pytest -v
```

Current verified result:

```text
12 passed
0 warnings
```

The tests cover:

- 5 Priority Queue cases
- 4 Dijkstra cases
- 3 Resource Allocation cases

---

## 13. Testing Summary

| Area | Test Cases |
|---|---:|
| Priority Queue | 5 |
| Dijkstra | 4 |
| Resource Allocation | 3 |
| **Total** | **12** |

Important tested scenarios include:

- Critical emergency receives higher priority.
- All severity levels are ordered correctly.
- Earlier emergency wins for equal severity.
- Empty queue behaves correctly.
- Queue size is maintained.
- Shortest graph route is calculated.
- Direct route is handled.
- Unreachable destination is detected.
- Same source/destination returns distance zero.
- Correct resource type is selected.
- Nearest suitable resource is selected.
- Busy/unavailable resources are ignored.

---

## 14. Academic Concepts Demonstrated

The project provides practical examples of:

- Python programming
- Object-oriented programming
- Abstract data structures
- Dictionaries and mappings
- Priority queues
- Heaps
- Graphs
- Shortest-path algorithms
- Sorting/selection logic
- Relational database concepts
- Primary and foreign keys
- CRUD operations
- REST APIs
- ORM-based database access
- Layered system architecture
- Software testing
- Frontend-backend integration

---

## 15. Limitations

The current system is intentionally an academic prototype.

It does not currently provide:

- live GPS vehicle tracking,
- live traffic information,
- integration with emergency-service infrastructure,
- real emergency communications,
- production-grade authentication,
- guaranteed real-world ETA,
- live external map routing,
- autonomous dispatch decisions in real emergency environments.

Route distances are stored as prototype graph data rather than obtained from a live mapping provider.

---

## 16. Future Enhancements

Possible extensions include:

- Live GPS tracking.
- Map-based visualization.
- Traffic-aware routing.
- WebSocket-based real-time updates.
- Mobile application.
- SMS/email notifications.
- Role-based authentication and authorization.
- Cloud deployment.
- Audit logs.
- More advanced resource optimization.
- Historical response analytics.
- Predictive analytics using historical emergency data.

---

## 17. Documentation

Detailed technical documentation is available in:

```text
docs/PROJECT_DOCUMENTATION.md
```

It covers requirements, architecture, modules, database design, algorithms, API behavior, testing, complexity, limitations, and future scope.

---

## 18. Disclaimer

This project is an academic software prototype and decision-support simulation. It must not be used as a replacement for real emergency dispatch, medical response, police response, fire response, or public-safety infrastructure.
