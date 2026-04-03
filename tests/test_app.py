from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_programs():
    client = app.test_client()
    response = client.get("/programs")
    assert response.status_code == 200


def test_calculate_calories_valid():
    client = app.test_client()

    response = client.post("/calculate-calories", json={
        "program": "fat_loss",
        "base_calories": 2000
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["recommended_calories"] == 1600


def test_calculate_calories_invalid_program():
    client = app.test_client()

    response = client.post("/calculate-calories", json={
        "program": "invalid",
        "base_calories": 2000
    })

    assert response.status_code == 400


def test_add_client():
    client = app.test_client()

    response = client.post("/add-client", json={
        "name": "Chirag",
        "program": "fat_loss",
        "calories": 1800
    })

    assert response.status_code == 201


def test_add_client_missing_fields():
    client = app.test_client()

    response = client.post("/add-client", json={
        "name": "Chirag"
    })

    assert response.status_code == 400


def test_get_clients():
    client = app.test_client()
    response = client.get("/clients")
    assert response.status_code == 200