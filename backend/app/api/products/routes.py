from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, validate
from app.schemas.product import ProductSchema, ProductListResponseSchema
from app.services.product_service import ProductService

products_bp = Blueprint("products", __name__)


class ListProductsQuery(Schema):
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=10, validate=validate.Range(min=1, max=100))
    location = fields.Str(load_default=None, validate=validate.OneOf(["JO", "SA"]))


@products_bp.route("", methods=["GET"])
@products_bp.doc(security=[{"BearerAuth": []}])
@products_bp.arguments(ListProductsQuery, location="query")
@products_bp.response(200, ProductListResponseSchema)
@products_bp.alt_response(401, description="Missing or invalid token")
@jwt_required()
def list_products(args):
    page = args.get("page", 1)
    per_page = args.get("per_page", 10)
    location = args.get("location")

    items, total = ProductService.list_products(
        page=page, per_page=per_page, location=location
    )
    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return {
        "items": [ProductSchema().dump(p) for p in items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages,
        },
    }


@products_bp.route("/<int:product_id>", methods=["GET"])
@products_bp.doc(security=[{"BearerAuth": []}])
@products_bp.response(200, ProductSchema)
@products_bp.alt_response(401, description="Missing or invalid token")
@products_bp.alt_response(404, description="Product not found")
@jwt_required()
def get_product(product_id):
    product = ProductService.get_product(product_id)
    if not product:
        abort(404, message="Product not found.")
    return ProductSchema().dump(product)
