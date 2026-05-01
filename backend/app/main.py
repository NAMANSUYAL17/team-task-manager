from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, projects, tasks, dashboard

# Create all DB tables automatically on startup (if they don't exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Team Task Manager", version="1.0.0")

# CORS allows your React frontend (localhost:5173) to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://69f527f8634f87868ea780e2--beautiful-dieffenbachia-c12791.netlify.app"
    ],        # in production, set this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers - each adds a group of endpoints
app.include_router(auth.router)       # /api/auth/signup, /api/auth/login
app.include_router(projects.router)   # /api/projects/
app.include_router(tasks.router)      # /api/tasks/
app.include_router(dashboard.router)  # /api/dashboard/

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Team Task Manager API running"}