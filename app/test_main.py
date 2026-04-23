import pytest
from fastapi.testclient import TestClient
from app.main import app, get_db
from app.database import Base, engine, SessionLocal

# On force la création des tables SQLite pour le test
Base.metadata.create_all(bind=engine)

# Override pour utiliser la session de test
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- LES TESTS ---

def test_signup_valid_domain():
    response = client.post(
        "/signup",
        json={"email": "test@inpt.ac.ma", "password": "password123", "full_name": "Test User"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@inpt.ac.ma"

def test_signup_invalid_domain():
    response = client.post(
        "/signup",
        json={"email": "hacker@gmail.com", "password": "password123", "full_name": "Hacker"}
    )
    # Doit être rejeté par le validateur Pydantic
    assert response.status_code == 422 

def test_login_and_create_trip():
    # 1. Créer l'utilisateur
    client.post(
        "/signup",
        json={"email": "said@inpt.ac.ma", "password": "securepassword", "full_name": "Said"}
    )
    
    # 2. Se connecter pour avoir le token
    login_response = client.post(
        "/login",
        data={"username": "said@inpt.ac.ma", "password": "securepassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Créer un trajet avec le token
    trip_response = client.post(
        "/trips/",
        json={"destination": "Casablanca", "date": "2026-05-10"},
        headers=headers
    )
    assert trip_response.status_code == 200
    assert trip_response.json()["destination"] == "Casablanca"

def test_create_trip_unauthorized():
    # Tester qu'on ne peut PAS créer sans token
    response = client.post(
        "/trips/",
        json={"destination": "Rabat", "date": "2026-05-12"}
    )
    assert response.status_code == 401