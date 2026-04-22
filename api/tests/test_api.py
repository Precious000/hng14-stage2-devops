from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch

client = TestClient(app)

# Mock redis BEFORE tests run
@patch("api.main.r")
def test_create_job(mock_redis):
    mock_redis.lpush.return_value = 1

    response = client.post("/jobs")

    assert response.status_code in [200, 201]
    mock_redis.lpush.assert_called_once()


@patch("api.main.r")
def test_get_job(mock_redis):
    mock_redis.get.return_value = b"done"

    response = client.get("/jobs/1")

    assert response.status_code == 200
