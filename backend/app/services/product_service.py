from typing import Optional, List, Tuple
from app.extensions import db
from app.models.product import Product


class ProductService:
    VALID_LOCATIONS = ("JO", "SA")

    @staticmethod
    def list_products(
        page: int = 1,
        per_page: int = 10,
        location: Optional[str] = None,
    ) -> Tuple[List[Product], int]:
        query = Product.query

        if location:
            if location not in ProductService.VALID_LOCATIONS:
                raise ValueError(f"Invalid location: {location}. Must be one of: JO, SA")
            query = query.filter(Product.location == location)

        query = query.order_by(Product.id.asc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total

    @staticmethod
    def get_product(product_id: int) -> Optional[Product]:
        return db.session.get(Product, product_id)
