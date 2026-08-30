from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_readiness():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready"
    }


def test_create_order():
    response = client.post(
        "/orders",
        json={
            "customer_id": "customer-123",
            "product_id": "product-456",
            "quantity": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer_id"] == "customer-123"
    assert data["product_id"] == "product-456"
    assert data["quantity"] == 2
    assert data["status"] == "created"


def test_order_not_found():
    response = client.get("/orders/does-not-exist")

    assert response.status_code == 404