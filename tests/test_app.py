from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_programs():
    client = app.test_client()
    response = client.get("/programs")
    assert response.status_code == 200


def test_calculate_calories():
    client = app.test_client()

    response = client.post("/calculate-calories", json={
        "program": "fat_loss",
        "base_calories": 2000
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["recommended_calories"] == 1600