# The central point and main command center of the project's API.
from fastapi import FastAPI
from .routers import workspace_router

app = FastAPI(
    title="ArgusScope API",
    description="API for the ArgusScope Reconnaissance Platform",
    version="0.1.0"
)

# Connect the workspace router to the main application.

app.include_router(workspace_router.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to ArgusScope API"}
