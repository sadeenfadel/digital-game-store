import pytest


class TestAuth:
    """Tests for authentication endpoints."""

    def test_valid_login(self, client, demo_user):
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "testpass123"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"

    def test_invalid_password(self, client, demo_user):
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data

    def test_nonexistent_user(self, client, demo_user):
        response = client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "testpass123"},
        )
        assert response.status_code == 401

    def test_missing_email(self, client, demo_user):
        response = client.post(
            "/api/auth/login",
            json={"password": "testpass123"},
        )
        assert response.status_code == 422

    def test_missing_password(self, client, demo_user):
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com"},
        )
        assert response.status_code == 422

    def test_missing_authentication(self, client):
        response = client.get("/api/products")
        assert response.status_code == 401

    def test_invalid_token(self, client):
        response = client.get(
            "/api/products",
            headers={"Authorization": "Bearer invalidtoken123"},
        )
        assert response.status_code == 422

    def test_get_current_user(self, client, auth_headers):
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["email"] == "test@example.com"

    def test_empty_body(self, client):
        response = client.post("/api/auth/login", json={})
        assert response.status_code == 422
