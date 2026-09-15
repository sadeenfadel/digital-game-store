from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.order import CreateOrderSchema, OrderResponseSchema, OrderDetailSchema
from app.services.order_service import OrderService

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("", methods=["POST"])
@orders_bp.doc(security=[{"BearerAuth": []}])
@orders_bp.arguments(CreateOrderSchema)
@orders_bp.response(201, OrderResponseSchema)
@orders_bp.alt_response(400, description="Invalid request body")
@orders_bp.alt_response(401, description="Missing or invalid token")
@orders_bp.alt_response(404, description="Product not found")
@jwt_required()
def create_order(data):
    user_id = int(get_jwt_identity())
    try:
        order = OrderService.create_order(user_id=user_id, product_id=data["product_id"])
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            abort(404, message=error_msg)
        abort(400, message=error_msg)

    return {
        "id": order.id,
        "product_id": order.product_id,
        "product_title": order.product_title,
        "price": str(order.price_at_purchase),
        "location": order.product_location,
        "created_at": order.created_at.isoformat(),
    }


@orders_bp.route("/<int:order_id>", methods=["GET"])
@orders_bp.doc(security=[{"BearerAuth": []}])
@orders_bp.response(200, OrderDetailSchema)
@orders_bp.alt_response(401, description="Missing or invalid token")
@orders_bp.alt_response(404, description="Order not found")
@jwt_required()
def get_order(order_id):
    user_id = int(get_jwt_identity())
    order = OrderService.get_user_order(user_id=user_id, order_id=order_id)
    if not order:
        abort(404, message="Order not found.")
    return {
        "id": order.id,
        "product_id": order.product_id,
        "product_title": order.product_title,
        "price_at_purchase": str(order.price_at_purchase),
        "product_location": order.product_location,
        "created_at": order.created_at.isoformat(),
        "user_id": order.user_id,
    }
