from datetime import datetime, timedelta
import pytest


def create_table(client, name="Resv Table"):
    response = client.post("/tables/", json={
        "name": name,
        "seats": 2,
        "location": "Corner"
    })
    return response.json()["id"]


def test_create_reservation(client):
    table_id = create_table(client)
    start_time = datetime.utcnow().replace(microsecond=0)
    payload = {
        "customer_name": "Alice",
        "table_id": table_id,
        "reservation_time": start_time.isoformat(),
        "duration_minutes": 60
    }

    resv_response = client.post("/reservations/", json=payload)
    assert resv_response.status_code == 200
    data = resv_response.json()
    assert data["customer_name"] == "Alice"


def test_reservation_conflict(client):
    table_id = create_table(client, name="Conflict Table")
    now = datetime.utcnow().replace(microsecond=0)

    # первая бронь
    client.post("/reservations/", json={
        "customer_name": "User1",
        "table_id": table_id,
        "reservation_time": now.isoformat(),
        "duration_minutes": 60
    })

    # конфликтная бронь
    conflict_payload = {
        "customer_name": "User2",
        "table_id": table_id,
        "reservation_time": (now + timedelta(minutes=30)).isoformat(),
        "duration_minutes": 30
    }

    resv_response = client.post("/reservations/", json=conflict_payload)
    assert resv_response.status_code == 400
    assert "already reserved" in resv_response.json()["detail"]


def test_delete_reservation(client):
    table_id = create_table(client, name="Del Resv Table")
    start_time = datetime.utcnow().replace(microsecond=0)
    payload = {
        "customer_name": "Charlie",
        "table_id": table_id,
        "reservation_time": start_time.isoformat(),
        "duration_minutes": 30
    }

    resv_response = client.post("/reservations/", json=payload)
    assert resv_response.status_code == 200
    resv_id = resv_response.json()["id"]

    del_response = client.delete(f"/reservations/{resv_id}")
    assert del_response.status_code == 200
    assert del_response.json() == {"ok": True}
