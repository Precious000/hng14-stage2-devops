import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

with patch("redis.Redis", return_value=MagicMock()):
    from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_redis():
    mock = MagicMock()
    mock.ping.return_value = True
    mock.get.return_value = None
    mock.set.return_value = True
    with patch("main.redis_client", mock):
        yield mock


def test_health_check(mock_redis):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_job(mock_redis):
    mock_redis.set.return_value = True
    mock_redis.lpush.return_value = 1
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data


def test_get_job_not_found(mock_redis):
    mock_redis.get.return_value = None
    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 404


def test_get_job_status(mock_redis):
    import json
    mock_redis.get.return_value = json.dumps({"status": "pending", "id": "abc-123"})
    response = client.get("/jobs/abc-123")
    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_health_check_response_structure(mock_redis):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
