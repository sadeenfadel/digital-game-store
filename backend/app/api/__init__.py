from app.api.auth.routes import auth_bp
from app.api.products.routes import products_bp
from app.api.orders.routes import orders_bp

__all__ = ["auth_bp", "products_bp", "orders_bp"]
