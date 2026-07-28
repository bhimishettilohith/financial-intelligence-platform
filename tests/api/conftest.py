import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.api.main import app


@pytest.fixture
def client():
    return TestClient(app)
