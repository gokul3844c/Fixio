import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database import engine, Base
from backend.seed_data import seed_database
from backend.routers import auth, scan, components, chat, guides, marketplace, service_centers, user

# Create DB tables & Seed Data
Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(
    title="FixAI API",
    description="AI Electronics Damage Detection & Repair Backend API",
    version="1.0.0"
)

# Enable CORS for local testing & SPA frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(scan.router)
app.include_router(components.router)
app.include_router(chat.router)
app.include_router(guides.router)
app.include_router(marketplace.router)
app.include_router(service_centers.router)
app.include_router(user.router)

# Health Check
@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "FixAI Engine", "version": "1.0.0"}

# Static file serving for uploads & frontend SPA
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

