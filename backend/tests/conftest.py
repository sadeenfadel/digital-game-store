import pytest
from decimal import Decimal
from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app, db):
    return app.test_client()


@pytest.fixture
def demo_user(db):
    user = User(email="test@example.com")
    user.set_password("testpass123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def demo_product(db):
    product = Product(
        id=9999,
        title="Test Product",
        description="A test product",
        price=Decimal("49.99"),
        location="JO",
    )
    db.session.add(product)
    db.session.commit()
    return product


@pytest.fixture
def auth_headers(client, demo_user):
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def second_user(db):
    user = User(email="other@example.com")
    user.set_password("otherpass123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def second_auth_headers(client, second_user):
    response = client.post(
        "/api/auth/login",
        json={"email": "other@example.com", "password": "otherpass123"},
    )
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
