import pytest


class TestOrders:
    """Tests for order endpoints."""

    def test_successful_purchase(self, client, auth_headers, demo_product):
        response = client.post(
            "/api/orders",
            json={"product_id": demo_product.id},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.get_json()
        assert "id" in data
        assert data["product_id"] == demo_product.id
        assert data["product_title"] == "Test Product"
        assert data["price"] == "49.99"
        assert data["location"] == "JO"

    def test_nonexistent_product(self, client, auth_headers):
        response = client.post(
            "/api/orders",
            json={"product_id": 999999},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_unauthenticated_purchase(self, client, demo_product):
        response = client.post(
            "/api/orders",
            json={"product_id": demo_product.id},
        )
        assert response.status_code == 401

    def test_retrieve_own_order(self, client, auth_headers, demo_product):
        create_response = client.post(
            "/api/orders",
            json={"product_id": demo_product.id},
            headers=auth_headers,
        )
        order_id = create_response.get_json()["id"]

        response = client.get(
            f"/api/orders/{order_id}", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == order_id
        assert data["product_title"] == "Test Product"

    def test_cannot_retrieve_other_users_order(
        self, client, auth_headers, second_auth_headers, demo_product
    ):
        create_response = client.post(
            "/api/orders",
            json={"product_id": demo_product.id},
            headers=auth_headers,
        )
        order_id = create_response.get_json()["id"]

        response = client.get(
            f"/api/orders/{order_id}", headers=second_auth_headers
        )
        assert response.status_code == 404

    def test_price_at_purchase_stored(self, client, auth_headers, demo_product):
        response = client.post(
            "/api/orders",
            json={"product_id": demo_product.id},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["price"] == "49.99"

    def test_nonexistent_order(self, client, auth_headers):
        response = client.get("/api/orders/999999", headers=auth_headers)
        assert response.status_code == 404

    def test_invalid_product_id(self, client, auth_headers):
        response = client.post(
            "/api/orders",
            json={"product_id": "not_a_number"},
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_missing_product_id(self, client, auth_headers):
        response = client.post(
            "/api/orders",
            json={},
            headers=auth_headers,
        )
        assert response.status_code == 422
