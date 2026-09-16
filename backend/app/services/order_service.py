from typing import Optional, List, Tuple
from app.extensions import db
from app.models.product import Product
from app.models.order import Order


class OrderService:
    @staticmethod
    def create_order(user_id: int, product_id: int) -> Order:
        product = db.session.get(Product, product_id)
        if not product:
            raise ValueError("Product not found.")

        already_owned = Order.query.filter_by(
            user_id=user_id, product_id=product_id
        ).first()
        if already_owned:
            raise ValueError("You have already purchased this product.")

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

    @staticmethod
    def list_user_orders(
        user_id: int, page: int = 1, per_page: int = 10
    ) -> Tuple[List[Order], int]:
        query = (
            Order.query.filter_by(user_id=user_id)
            .order_by(Order.created_at.desc())
        )
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total
