from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.database import Base, engine

from app.models import (
    User,
    Location,
    Resource,
    Emergency,
    Route,
    Dispatch
)

from app.routes import (
    locations,
    resources,
    emergencies,
    priority,
    routes,
    dispatches,
    dispatch_tracking
)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Smart Emergency Response System",
    description="Emergency response and resource management system",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory="app/templates"
)


# API routes
app.include_router(locations.router)
app.include_router(resources.router)
app.include_router(emergencies.router)
app.include_router(priority.router)
app.include_router(routes.router)
app.include_router(dispatches.router)
app.include_router(dispatch_tracking.router)


# Dashboard
@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request}
    )