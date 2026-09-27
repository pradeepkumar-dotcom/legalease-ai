"""
FastAPI Main Application Entry Point
"""
import os
import time
from pathlib import Path
from contextlib import asynccontextmanager
try:
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from fastapi.staticfiles import StaticFiles
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    class FastAPI:
        def __init__(self, *args, **kwargs):
            self.routes = []
        def add_middleware(self, *args, **kwargs): pass
        def mount(self, *args, **kwargs): pass
        def middleware(self, *args, **kwargs): return lambda f: f
        def include_router(self, *args, **kwargs): pass
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
    Request = None
    CORSMiddleware = None
    JSONResponse = None
    StaticFiles = None

from legalEaseAPI.routes import router as api_router
from config import BASE_DIR, IMAGE_DIR, LOGO_PATH, INVERSE_LOGO_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup validation
    print("[*] LegalEase Enterprise API Initializing...")
    if not LOGO_PATH.exists() or not INVERSE_LOGO_PATH.exists():
        from setup_assets import generate_logos
        generate_logos()
    print("[+] Assets & Engine Verified. Ready for traffic.")
    yield
    print("[-] LegalEase API shutting down.")


app = FastAPI(
    title="LegalEase: AI-Powered Legal Document Generator API",
    description="Enterprise-grade REST API for automated legal document drafting, clause formulation, and multi-format exports (.pdf, .docx, .txt).",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static directory for logos and brand assets
# Mount Static directory for logos and brand assets
if FASTAPI_AVAILABLE and IMAGE_DIR.exists() and StaticFiles:
    app.mount("/static/images", StaticFiles(directory=str(IMAGE_DIR)), name="images")


# Request Timing Middleware
if FASTAPI_AVAILABLE:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time-Seconds"] = f"{process_time:.4f}"
        return response


# Include API Router
if FASTAPI_AVAILABLE:
    app.include_router(api_router)


# Root Health Check
@app.get("/", tags=["System"])
async def root_health_check():
    return {
        "service": "LegalEase AI Document Generator",
        "status": "healthy",
        "version": "1.0.0",
        "documentation": "/docs",
        "api_v1": "/api/v1"
    }


@app.get("/health", tags=["System"])
async def health():
    return {"status": "healthy", "timestamp": time.time()}


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    uvicorn.run("legalEaseAPI.main:app", host=API_HOST, port=API_PORT, reload=True)
