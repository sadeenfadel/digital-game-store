from datetime import datetime, timezone
from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    product_title = db.Column(db.String(255), nullable=False)
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)
    product_location = db.Column(db.String(2), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship("User", back_populates="orders")
    product = db.relationship("Product", back_populates="orders")

    __table_args__ = (
        db.Index("idx_orders_user_id", "user_id"),
        db.Index("idx_orders_product_id", "product_id"),
    )

    def __repr__(self) -> str:
        return f"<Order {self.id}>"
