from fastapi.testclient import TestClient
from api.main import app   # FIXED IMPORT PATH

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_get_job():
    res = client.post("/jobs")
    job_id = res.json()["job_id"]

    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
