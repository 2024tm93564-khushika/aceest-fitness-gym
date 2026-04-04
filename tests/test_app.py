import pytest
from app import app


# ── Fixture ───────────────────────────────────────────────────────────────────
# Provides a fresh test client for every test function
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ── Home ──────────────────────────────────────────────────────────────────────
def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


# ── Create Client ─────────────────────────────────────────────────────────────
def test_create_client_success(client):
    response = client.post("/clients", json={
        "name": "Priya",
        "program": "fat_loss",
        "calories": 2000
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Client saved"


def test_create_client_invalid_program(client):
    response = client.post("/clients", json={
        "name": "Test",
        "program": "invalid_program",
        "calories": 2000
    })
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_client_empty_name(client):
    response = client.post("/clients", json={
        "name": "",
        "program": "fat_loss",
        "calories": 2000
    })
    assert response.status_code == 400


def test_create_client_negative_calories(client):
    response = client.post("/clients", json={
        "name": "Test",
        "program": "fat_loss",
        "calories": -100
    })
    assert response.status_code == 400


# ── Get All Clients ───────────────────────────────────────────────────────────
def test_get_all_clients(client):
    response = client.get("/clients")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


# ── Get Client by Name ────────────────────────────────────────────────────────
def test_get_client_found(client):
    # First create the client
    client.post("/clients", json={
        "name": "Rahul",
        "program": "muscle_gain",
        "calories": 3200
    })
    # Then retrieve it
    response = client.get("/clients/Rahul")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Rahul"
    assert data["program"] == "muscle_gain"


def test_get_client_not_found(client):
    response = client.get("/clients/DoesNotExist")
    assert response.status_code == 404
    assert "error" in response.get_json()


# ── Delete Client ─────────────────────────────────────────────────────────────
def test_delete_client(client):
    # Create first, then delete — self-contained test
    client.post("/clients", json={
        "name": "ToDelete",
        "program": "beginner",
        "calories": 1800
    })
    response = client.delete("/clients/ToDelete")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Client deleted"


# ── Progress ──────────────────────────────────────────────────────────────────
def test_add_progress_success(client):
    response = client.post("/progress", json={
        "name": "Priya",
        "week": "Week-1",
        "adherence": 90
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Progress saved"


def test_get_progress_found(client):
    # Add progress first
    client.post("/progress", json={
        "name": "ProgressUser",
        "week": "Week-1",
        "adherence": 75
    })
    response = client.get("/progress/ProgressUser")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["adherence"] == 75


def test_get_progress_not_found(client):
    response = client.get("/progress/NoSuchUser")
    assert response.status_code == 404


def test_add_progress_invalid_adherence(client):
    # Adherence must be 0–100
    response = client.post("/progress", json={
        "name": "Test",
        "week": "Week-1",
        "adherence": 150
    })
    assert response.status_code == 400


def test_add_progress_missing_week(client):
    response = client.post("/progress", json={
        "name": "Test",
        "week": "",
        "adherence": 80
    })
    assert response.status_code == 400


# ── Calculate Calories ────────────────────────────────────────────────────────
def test_calories_fat_loss(client):
    response = client.post("/calculate-calories", json={
        "program": "fat_loss",
        "base_calories": 2000
    })
    assert response.status_code == 200
    # fat_loss multiplier is 0.8
    assert response.get_json()["recommended_calories"] == 1600.0


def test_calories_muscle_gain(client):
    response = client.post("/calculate-calories", json={
        "program": "muscle_gain",
        "base_calories": 2000
    })
    assert response.status_code == 200
    # muscle_gain multiplier is 1.2
    assert response.get_json()["recommended_calories"] == 2400.0


def test_calories_beginner(client):
    response = client.post("/calculate-calories", json={
        "program": "beginner",
        "base_calories": 2000
    })
    assert response.status_code == 200
    # beginner multiplier is 1.0 — no change
    assert response.get_json()["recommended_calories"] == 2000.0


def test_calories_invalid_program(client):
    response = client.post("/calculate-calories", json={
        "program": "invalid",
        "base_calories": 2000
    })
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_calories_invalid_type(client):
    response = client.post("/calculate-calories", json={
        "program": "fat_loss",
        "base_calories": "not_a_number"
    })
    assert response.status_code == 400