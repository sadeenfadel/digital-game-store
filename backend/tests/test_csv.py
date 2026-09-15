import pytest
import tempfile
import os
from decimal import Decimal
from app.extensions import db as _db
from app.models.product import Product
from scripts.import_csv import validate_row


class TestCSVValidation:
    """Tests for CSV row validation."""

    def test_validate_row_valid(self):
        row = {
            "id": "1",
            "title": "Test Game",
            "description": "A test game",
            "price": "29.99",
            "location": "JO",
        }
        errors = validate_row(row, 1)
        assert errors == []

    def test_validate_row_missing_id(self):
        row = {"title": "Test Game", "price": "29.99", "location": "JO"}
        errors = validate_row(row, 1)
        assert any("Missing 'id'" in e for e in errors)

    def test_validate_row_invalid_id(self):
        row = {"id": "abc", "title": "Test Game", "price": "29.99", "location": "JO"}
        errors = validate_row(row, 1)
        assert any("Invalid 'id'" in e for e in errors)

    def test_validate_row_missing_title(self):
        row = {"id": "1", "price": "29.99", "location": "JO"}
        errors = validate_row(row, 1)
        assert any("Missing 'title'" in e for e in errors)

    def test_validate_row_invalid_price(self):
        row = {"id": "1", "title": "Test", "price": "abc", "location": "JO"}
        errors = validate_row(row, 1)
        assert any("Invalid 'price'" in e for e in errors)

    def test_validate_row_invalid_location(self):
        row = {"id": "1", "title": "Test", "price": "29.99", "location": "XX"}
        errors = validate_row(row, 1)
        assert any("Invalid 'location'" in e for e in errors)

    def test_validate_row_valid_sa(self):
        row = {
            "id": "2",
            "title": "Test Game 2",
            "price": "19.99",
            "location": "SA",
        }
        errors = validate_row(row, 1)
        assert errors == []


class TestCSVImport:
    """Tests for CSV import functionality using test database."""

    def test_import_creates_products(self, app, db):
        with app.app_context():
            from scripts.import_csv import import_csv as do_import

            csv_content = "id,title,description,price,location\n8001,Game One,Desc,10.00,JO\n8002,Game Two,Desc,20.00,SA\n"
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f:
                f.write(csv_content)
                csv_path = f.name

            try:
                do_import(csv_path)
                count = _db.session.query(Product).filter(Product.id.in_([8001, 8002])).count()
                assert count == 2
            finally:
                _db.session.query(Product).filter(Product.id.in_([8001, 8002])).delete()
                _db.session.commit()
                os.unlink(csv_path)

    def test_import_idempotent(self, app, db):
        with app.app_context():
            from scripts.import_csv import import_csv as do_import

            csv_content = "id,title,description,price,location\n8003,Game One,Desc,10.00,JO\n"
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f:
                f.write(csv_content)
                csv_path = f.name

            try:
                do_import(csv_path)
                do_import(csv_path)
                count = _db.session.query(Product).filter(Product.id == 8003).count()
                assert count == 1
            finally:
                _db.session.query(Product).filter(Product.id == 8003).delete()
                _db.session.commit()
                os.unlink(csv_path)
