from app import app


def test_home():
    client = app.test_client()
    assert client.get("/").status_code == 200


def test_valid_client():
    client = app.test_client()
    response = client.post("/add-client", json={
        "name": "Chirag",
        "program": "fat_loss",
        "calories": 1800
    })
    assert response.status_code == 201


def test_invalid_program():
    client = app.test_client()
    response = client.post("/add-client", json={
        "name": "Test",
        "program": "invalid",
        "calories": 1800
    })
    assert response.status_code == 400


def test_invalid_calories():
    client = app.test_client()
    response = client.post("/add-client", json={
        "name": "Test",
        "program": "fat_loss",
        "calories": -100
    })
    assert response.status_code == 400


def test_calculate_valid():
    client = app.test_client()
    response = client.post("/calculate-calories", json={
        "program": "fat_loss",
        "base_calories": 2000
    })
    assert response.status_code == 200