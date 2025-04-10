import pytest


def test_create_table(client):
    response = client.post("/tables/", json={
        "name": "Test Table",
        "seats": 4,
        "location": "Test Room"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Table"
    assert data["seats"] == 4


def test_get_tables(client):
    response = client.get("/tables/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_table_without_reservation(client):
    response = client.post("/tables/", json={
        "name": "Deletable Table",
        "seats": 2,
        "location": "Nowhere"
    })
    table_id = response.json()["id"]

    response = client.delete(f"/tables/{table_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_delete_table_with_reservation(client):
    # Создание стола
    response = client.post("/tables/", json={
        "name": "Reserved Table",
        "seats": 2,
        "location": "VIP"
    })
    table_id = response.json()["id"]

    # Создание брони
    from datetime import datetime
    start_time = datetime.utcnow().replace(microsecond=0)
    resv_response = client.post("/reservations/", json={
        "customer_name": "Deny",
        "table_id": table_id,
        "reservation_time": start_time.isoformat(),
        "duration_minutes": 60
    })
    assert resv_response.status_code == 200

    # Попытка удалить стол
    del_response = client.delete(f"/tables/{table_id}")
    assert del_response.status_code == 400
    assert "active reservations" in del_response.json()["detail"]
