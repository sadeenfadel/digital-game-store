#!/usr/bin/env python3
"""CSV Import Script for Digital Game Store.

Reads products from a CSV file and imports them into PostgreSQL.
Use idempotent behavior: INSERT if new, UPDATE if existing.

Usage:
    cd backend
    python scripts/import_csv.py [csv_file_path]
"""

import csv
import sys
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.extensions import db
from app.models.product import Product

DEFAULT_CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "items.csv"
)

VALID_LOCATIONS = ("JO", "SA")


def validate_row(row: dict, row_num: int) -> list[str]:
    errors = []

    if not row.get("id"):
        errors.append(f"Row {row_num}: Missing 'id'")
    else:
        try:
            int(row["id"])
        except ValueError:
            errors.append(f"Row {row_num}: Invalid 'id' '{row['id']}' - must be integer")

    if not row.get("title"):
        errors.append(f"Row {row_num}: Missing 'title'")

    if not row.get("price"):
        errors.append(f"Row {row_num}: Missing 'price'")
    else:
        try:
            Decimal(row["price"])
        except InvalidOperation:
            errors.append(f"Row {row_num}: Invalid 'price' '{row['price']}' - must be numeric")

    if not row.get("location"):
        errors.append(f"Row {row_num}: Missing 'location'")
    elif row["location"] not in VALID_LOCATIONS:
        errors.append(
            f"Row {row_num}: Invalid 'location' '{row['location']}' - must be JO or SA"
        )

    return errors


def import_csv(csv_path: str) -> None:
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)

    created = 0
    updated = 0
    failed = 0
    total = 0
    all_errors = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            total += 1
            errors = validate_row(row, row_num)
            if errors:
                all_errors.extend(errors)
                failed += 1
                continue

            product_id = int(row["id"])
            title = row["title"].strip()
            description = row.get("description", "").strip() or None
            price = Decimal(row["price"])
            location = row["location"].strip()

            existing = db.session.get(Product, product_id)
            if existing:
                existing.title = title
                existing.description = description
                existing.price = price
                existing.location = location
                updated += 1
            else:
                product = Product(
                    id=product_id,
                    title=title,
                    description=description,
                    price=price,
                    location=location,
                )
                db.session.add(product)
                created += 1

    db.session.commit()

    print(f"\nImport Summary:")
    print(f"  Total rows processed: {total}")
    print(f"  Created: {created}")
    print(f"  Updated: {updated}")
    print(f"  Failed: {failed}")

    if all_errors:
        print(f"\nErrors:")
        for err in all_errors:
            print(f"  - {err}")


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV_PATH
    print(f"Importing products from: {csv_path}")

    from app import create_app

    app = create_app()
    with app.app_context():
        import_csv(csv_path)


if __name__ == "__main__":
    main()
