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

@app.on_event("startup")
def on_startup() -> None:
    """Create tables if they do not exist (local/dev only)."""
    init_db()

@app.get("/")
def healthcheck():
    """Simple health endpoint."""
    return {"status": "ok", "app": settings.APP_NAME}