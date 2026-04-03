from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_add_client():
    client = app.test_client()

    response = client.post("/add-client", json={
        "name": "Chirag",
        "program": "fat_loss",
        "calories": 1800
    })

    assert response.status_code == 201


def test_get_clients():
    client = app.test_client()
    response = client.get("/clients")
    assert response.status_code == 200


def test_calculate_calories():
    client = app.test_client()

    response = client.post("/calculate-calories", json={
        "program": "fat_loss",
        "base_calories": 2000
    })

    assert response.status_code == 200