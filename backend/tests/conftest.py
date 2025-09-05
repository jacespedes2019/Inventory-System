import sys, pathlib
import uuid
ROOT = pathlib.Path(__file__).resolve().parents[1]  # .../backend
sys.path.insert(0, str(ROOT))


import os
import sys
import pathlib
import typing as t

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool  # <-- use StaticPool

# Ensure backend root is on sys.path (backend/ contains app/ and tests/)
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Import the FastAPI app and deps AFTER sys.path fix
from app.main import app
from app.db.base import Base
from app.deps import get_db

# IMPORTANT: import models so Base.metadata knows about tables
from app.models import user as user_model  # noqa: F401
from app.models import product as product_model  # noqa: F401


# --- Configure environment for tests ---
os.environ["APP_ENV"] = "test"

# --- Single in-memory SQLite connection for the entire test session ---
# StaticPool makes all connections go to the same in-memory DB.
TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # <-- key change
)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(autouse=True)
def clean_db():
    # Use a single transaction to clear tables in the right order
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM products"))
        conn.execute(text("DELETE FROM users"))

@pytest.fixture(scope="session", autouse=True)
def create_test_db_schema():
    """Create all tables once for the test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    """Provide a database session per test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# --- Override app.get_db to use the testing session ---
def _override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# Disable startup init_db(): avoid touching the real DB
app.router.on_startup = []
app.dependency_overrides[get_db] = _override_get_db

@pytest.fixture()
def client() -> TestClient:
    """FastAPI TestClient that uses the overridden DB dependency."""
    with TestClient(app) as c:
        yield c


# --- Helper functions ---
def _unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"

def _register(client: TestClient, email: str, password: str, role: str = "user"):
    r = client.post("/auth/register", json={"email": email, "password": password, "role": role})
    # si ya existe, está bien para tests; no falles por eso
    if r.status_code not in (201, 400):
        assert False, r.text
    return r

def _login(client: TestClient, email: str, password: str) -> str:
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]

@pytest.fixture()
def user_token(client: TestClient) -> str:
    email, pwd = _unique_email("user"), "secret123"
    _register(client, email, pwd, role="user")
    return _login(client, email, pwd)

@pytest.fixture()
def admin_token(client: TestClient) -> str:
    email, pwd = _unique_email("admin"), "secret123"
    _register(client, email, pwd, role="admin")
    return _login(client, email, pwd)