from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch

client = TestClient(app)


@patch("api.main.r")
def test_health(mock_redis):
    res = client.get("/health")
    assert res.status_code == 200


@patch("api.main.r")
def test_create_job(mock_redis):
    res = client.post("/jobs")
    assert res.status_code == 200
    assert "job_id" in res.json()


@patch("api.main.r")
def test_get_job(mock_redis):
    job_id = "123"
    mock_redis.hget.return_value = "completed"

    res = client.get(f"/jobs/{job_id}")
    assert res.status_code == 200
