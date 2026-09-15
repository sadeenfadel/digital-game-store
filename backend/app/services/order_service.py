from typing import Optional
from app.extensions import db
from app.models.product import Product
from app.models.order import Order


class OrderService:
    @staticmethod
    def create_order(user_id: int, product_id: int) -> Order:
        product = db.session.get(Product, product_id)
        if not product:
            raise ValueError("Product not found.")

        order = Order(
            user_id=user_id,
            product_id=product.id,
            product_title=product.title,
            price_at_purchase=product.price,
            product_location=product.location,
        )
        db.session.add(order)
        db.session.commit()
        return order

    @staticmethod
    def get_user_order(user_id: int, order_id: int) -> Optional[Order]:
        return Order.query.filter_by(id=order_id, user_id=user_id).first()
