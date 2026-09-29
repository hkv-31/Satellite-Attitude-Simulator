from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_simulate():
    response = client.post(
        "/simulate",
        json={
            "target_angle": 0,
            "start_angle": 45,
            "start_angular_velocity": 0,
            "max_steps": 50,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert "final_angle" in data
