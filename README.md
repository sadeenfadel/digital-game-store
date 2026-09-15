# Digital Game Store

A full-stack Digital Game Store application consisting of two independent applications:

* **Backend:** Python Flask REST API with JWT authentication, product management, order processing, CSV import, and Swagger/OpenAPI documentation.
* **Frontend:** React + TypeScript single-page application with authentication, product browsing, purchasing, and receipt display.

## Architecture

```text
┌─────────────────┐         HTTP/JSON         ┌─────────────────┐
│                 │ ◄──────────────────────► │                 │
│    Frontend     │                          │     Backend     │
│   React/Vite    │                          │   Flask API     │
│   Port: 5173    │                          │   Port: 5000    │
│                 │                          │                 │
└─────────────────┘                          └────────┬────────┘
                                                     │
                                                     │ SQLAlchemy
                                                     ▼
                                             ┌─────────────────┐
                                             │     SQLite      │
                                             │    Database     │
                                             └─────────────────┘
```

The frontend and backend communicate exclusively through HTTP/JSON REST APIs.

## Backend

* Python 3.11+
* Flask
* Flask application factory pattern
* SQLAlchemy ORM with Flask-SQLAlchemy
* Alembic/Flask-Migrate for database migrations
* JWT authentication
* Swagger/OpenAPI documentation
* SQLite database
* CSV product import
* Pytest tests

See [backend/README.md](backend/README.md) for detailed backend setup instructions.

## Frontend

* React 18
* TypeScript
* Vite
* React Router
* Axios
* CSS Modules

See [frontend/README.md](frontend/README.md) for detailed frontend setup instructions.

## Getting Started

### Prerequisites

Make sure the following are installed:

* Python 3.11+
* Node.js 18+
* npm

SQLite does **not** require a separate database server.

## Backend Setup

```bash
cd backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
```

Configure the local environment values in `.env`.

The application uses SQLite, so no PostgreSQL installation is required.

### Run Database Migrations

```bash
flask db upgrade
```

### Import Products

The project includes the provided CSV file at:

```text
backend/data/items.csv
```

Import the products with:

```bash
python scripts/import_csv.py
```

### Create Demo User

Create the demo login account:

```bash
python scripts/seed_demo_user.py
```

Use the credentials documented by the seed script/README.

### Start the Backend

```bash
flask run
```

The API will normally be available at:

```text
http://localhost:5000
```

Swagger/OpenAPI documentation is available at the URL configured by the backend application.

## Frontend Setup

Open a new terminal:

```bash
cd frontend

npm install

cp .env.example .env
```

Configure:

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

Then start the frontend:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

## Application Flow

```text
Login
  ↓
JWT authentication
  ↓
Product listing
  ↓
JO / SA location filtering
  ↓
Pagination
  ↓
Product details
  ↓
Purchase
  ↓
Order creation
  ↓
Receipt
```

## API

Main endpoints:

```text
POST /api/auth/login

GET  /api/products
GET  /api/products/{product_id}

POST /api/orders
GET  /api/orders/{order_id}
```

Protected endpoints require:

```text
Authorization: Bearer <JWT>
```

## Testing

### Backend

From the `backend` directory:

```bash
pytest
```

### Frontend

Run the available lint/build checks:

```bash
npm run lint
npm run build
```

## Environment Variables

Do not commit real `.env` files or secrets.

The repository includes:

```text
backend/.env.example
frontend/.env.example
```

Create local `.env` files from these examples.

## Project Structure

```text
digital-game-store/
├── backend/
│   ├── app/
│   ├── data/
│   │   └── items.csv
│   ├── migrations/
│   ├── scripts/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── README.md
│
├── .gitignore
└── README.md
```
