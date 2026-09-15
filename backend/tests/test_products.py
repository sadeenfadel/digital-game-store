import pytest


class TestProducts:
    """Tests for product endpoints."""

    def test_list_products(self, client, auth_headers, demo_product):
        response = client.get("/api/products", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert "items" in data
        assert "pagination" in data
        assert data["pagination"]["total"] >= 1

    def test_pagination(self, client, auth_headers, demo_product):
        response = client.get(
            "/api/products?page=1&per_page=5", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["per_page"] == 5
        assert len(data["items"]) <= 5

    def test_filter_jo(self, client, auth_headers, demo_product):
        response = client.get("/api/products?location=JO", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        for item in data["items"]:
            assert item["location"] == "JO"

    def test_filter_sa(self, client, auth_headers, demo_product):
        response = client.get("/api/products?location=SA", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        for item in data["items"]:
            assert item["location"] == "SA"

    def test_invalid_location(self, client, auth_headers, demo_product):
        response = client.get("/api/products?location=XX", headers=auth_headers)
        assert response.status_code == 422

    def test_get_product_detail(self, client, auth_headers, demo_product):
        response = client.get(
            f"/api/products/{demo_product.id}", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == demo_product.id
        assert data["title"] == "Test Product"

    def test_nonexistent_product(self, client, auth_headers):
        response = client.get("/api/products/999999", headers=auth_headers)
        assert response.status_code == 404

    def test_unauthenticated_list(self, client, demo_product):
        response = client.get("/api/products")
        assert response.status_code == 401

    def test_unauthenticated_detail(self, client, demo_product):
        response = client.get(f"/api/products/{demo_product.id}")
        assert response.status_code == 401

    def test_product_price_is_string(self, client, auth_headers, demo_product):
        response = client.get(
            f"/api/products/{demo_product.id}", headers=auth_headers
        )
        data = response.get_json()
        assert isinstance(data["price"], str)

    def test_pagination_per_page_max(self, client, auth_headers, demo_product):
        response = client.get(
            "/api/products?per_page=200", headers=auth_headers
        )
        assert response.status_code == 422
