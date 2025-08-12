import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure project root is on PYTHONPATH for `import app`
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")


@pytest.fixture()
def client() -> TestClient:
    from app.main import app

    return TestClient(app)


def make_jwt(sub: str) -> str:
    from jose import jwt
    from app.config import settings

    return jwt.encode({"sub": sub}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


@pytest.fixture()
def auth_header() -> dict[str, str]:
    token = make_jwt("test-user")
    return {"Authorization": f"Bearer {token}"}

