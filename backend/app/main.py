from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, projects, tasks, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Team Task Manager", version="1.0.0")

# Allow all origins temporarily to fix CORS - works for both local and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   # must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(dashboard.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Team Task Manager API running"}