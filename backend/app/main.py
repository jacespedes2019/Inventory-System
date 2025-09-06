"""
File: main.py
Description: FastAPI application entrypoint with middleware and route registration.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Initialize FastAPI instance with title and configuration.
- Configure CORS middleware for cross-origin requests.
- Include routers for authentication and product APIs.
- Run startup events such as database initialization.
- Provide healthcheck endpoint for monitoring.

Notes:
- API documentation available at /docs and /redoc.
- All routes are prefixed according to their domain (e.g., /auth, /products).
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, products
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(title=settings.APP_NAME)

# CORS: adjust origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to execute during startup
    """Create tables if they do not exist (local/dev only)."""
    init_db()
    yield
    # Code to execute during shutdown
    print("Application shutdown!")
    
@app.get("/")
def healthcheck():
    """Simple health endpoint."""
    return {"status": "ok", "app": settings.APP_NAME}