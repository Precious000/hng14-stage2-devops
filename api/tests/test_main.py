import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def mock_redis():
    mock = MagicMock()
    mock.ping.return_value = True
    mock.hget.return_value = None
    mock.hset.return_value = True
    mock.lpush.return_value = 1
    with patch("redis.Redis", return_value=mock):
        import importlib
        import main
        importlib.reload(main)
        from main import app
        with patch.object(main, "r", mock):
            yield mock


@pytest.fixture
def client(mock_redis):
    import main
    return TestClient(main.app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_job(client, mock_redis):
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert mock_redis.lpush.called
    assert mock_redis.hset.called


def test_get_job_not_found(client, mock_redis):
    mock_redis.hget.return_value = None
    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 200
    assert response.json() == {"error": "not found"}


def test_get_job_status(client, mock_redis):
    mock_redis.hget.return_value = "queued"
    response = client.get("/jobs/abc-123")
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
    assert response.json()["job_id"] == "abc-123"


def test_create_job_returns_uuid(client, mock_redis):
    response = client.post("/jobs")
    assert response.status_code == 200
    job_id = response.json()["job_id"]
    import uuid
    uuid.UUID(job_id)
