# Backend - Digital Game Store API

## Prerequisites

- Python 3.11+
- pip

SQLite is used - no database server required.

## Installation

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

## Database Setup

```bash
export FLASK_APP=run.py

# Create migration (first time only)
flask db init

# Apply migrations
flask db upgrade
```

This creates `data/game_store.db` automatically.

## Import Products

```bash
python scripts/import_csv.py
```

## Create Demo User

```bash
python scripts/seed_demo_user.py
```

**Demo credentials:**
- Email: `demo@gamstore.com`
- Password: `password123`

## Start the API

```bash
flask run
```

Runs at `http://localhost:5000`

## Swagger Documentation

Open `http://localhost:5000/api/docs/` in your browser.

## Health Check

```bash
curl http://localhost:5000/health
```

## Run Tests

```bash
python -m pytest tests/ -v
```

## Sample Usage

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@gamstore.com","password":"password123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# List products
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/products

# Filter by location
curl -H "Authorization: Bearer $TOKEN" "http://localhost:5000/api/products?location=JO"

# Buy a product
curl -X POST http://localhost:5000/api/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration (SQLite)
│   ├── extensions.py        # Flask extensions
│   ├── errors.py            # Error handlers
│   ├── api/                 # API routes
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Marshmallow schemas
│   ├── services/            # Business logic
│   └── docs/                # OpenAPI config
├── data/
│   ├── game_store.db        # SQLite database
│   └── items.csv            # Product data
├── migrations/              # Database migrations
├── scripts/
│   ├── import_csv.py        # CSV importer
│   └── seed_demo_user.py    # Demo user seeder
├── tests/                   # Test suite
├── requirements.txt
├── run.py
└── README.md
```
