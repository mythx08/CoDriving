from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_ride_quota_limit():
    user_id = "test_user_pro"
    ride_data = {
        "departure_zone": "Zone A",
        "destination_zone": "Zone B",
        "price": 20.0,
        "departure_time": "2026-04-21T10:00:00"
    }

    # On crée 4 trajets
    for i in range(4):
        response = client.post(f"/rides/?user_id={user_id}", json=ride_data)
        assert response.status_code == 201

    # Le 5ème doit être bloqué
    response = client.post(f"/rides/?user_id={user_id}", json=ride_data)
    assert response.status_code == 403