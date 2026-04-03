from app import app


def test_add_client():
    client = app.test_client()
    response = client.post("/add-client", json={
        "name": "Test",
        "program": "fat_loss",
        "calories": 1800
    })
    assert response.status_code == 201


def test_get_client():
    client = app.test_client()
    client.post("/add-client", json={
        "name": "Test",
        "program": "fat_loss",
        "calories": 1800
    })

    response = client.get("/client/Test")
    assert response.status_code == 200


def test_save_progress():
    client = app.test_client()
    response = client.post("/progress", json={
        "name": "Test",
        "week": "Week 1",
        "adherence": 80
    })
    assert response.status_code == 201


def test_calculate_calories():
    client = app.test_client()
    response = client.post("/calculate-calories", json={
        "program": "fat_loss",
        "base_calories": 2000
    })
    assert response.status_code == 200