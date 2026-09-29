import os
import time
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from backend.database import engine, Base
from backend.seed_data import seed_database
from backend.routers import auth, scan, components, chat, guides, marketplace, service_centers, user

# Create DB tables & Seed Data
Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(
    title="Fixio API",
    description="Fixio - Compound & Property Damage Detection, Repair Guides & Nearby Service Centers API",
    version="1.0.0"
)

# Rate Limiting Store
RATE_LIMIT_STORE = defaultdict(list)
RATE_LIMIT_MAX = 120 # requests per minute
RATE_LIMIT_WINDOW = 60 # seconds

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()
    
    timestamps = [t for t in RATE_LIMIT_STORE[client_ip] if now - t < RATE_LIMIT_WINDOW]
    RATE_LIMIT_STORE[client_ip] = timestamps

    if len(timestamps) >= RATE_LIMIT_MAX and request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=429,
            content={"success": False, "detail": "Rate limit exceeded. Too many requests. Please wait a minute."}
        )

    RATE_LIMIT_STORE[client_ip].append(now)
    response = await call_next(request)
    return response

# Centralized Error Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"success": False, "detail": "Request validation failed.", "errors": str(exc.errors())}
    )

# Enable CORS for local testing & SPA frontend
allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
if allowed_origins_env:
    origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
else:
    origins = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    return {"status": "ok", "service": "Fixio Engine", "version": "1.0.0"}


# Static file serving for uploads & frontend SPA
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

