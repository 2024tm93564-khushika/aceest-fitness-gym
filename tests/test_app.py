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
    response = client.get("/client/Test")
    assert response.status_code in [200, 404]


def test_progress_flow():
    client = app.test_client()

    client.post("/progress", json={
        "name": "Test",
        "week": "Week 1",
        "adherence": 80
    })

    response = client.get("/progress/Test")
    assert response.status_code in [200, 404]


def test_delete_client():
    client = app.test_client()
    response = client.delete("/client/Test")
    assert response.status_code == 200


def test_calories():
    client = app.test_client()
    response = client.post("/calculate-calories", json={
        "program": "fat_loss",
        "base_calories": 2000
    })
    assert response.status_code == 200