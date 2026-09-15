# Digital Game Store

A full-stack Digital Game Store application consisting of two independent applications:

- **Backend**: Python Flask API service with JWT authentication, product management, order processing, and Swagger/OpenAPI documentation
- **Frontend**: React (TypeScript) single-page application with authentication, product browsing, purchasing, and receipt display

## Architecture

```
┌─────────────────┐         HTTP/JSON         ┌─────────────────┐
│                  │ ◄──────────────────────► │                  │
│   Frontend       │                          │    Backend       │
│   (React/Vite)   │                          │   (Flask API)   │
│   Port: 5173     │                          │   Port: 5000     │
│                  │                          │                  │
└─────────────────┘                          └────────┬────────┘
                                                      │
                                                      │
                                              ┌───────▼────────┐
                                              │   PostgreSQL    │
                                              │   Database      │
                                              └────────────────┘
```

The backend and frontend communicate exclusively through HTTP/JSON REST APIs.

## Backend

- Python 3.11+
- Flask application factory pattern
- SQLAlchemy ORM with Flask-SQLAlchemy
- Alembic/Flask-Migrate for database migrations
- JWT authentication
- Swagger/OpenAPI documentation
- PostgreSQL database

See [backend/README.md](backend/README.md) for setup instructions.

## Frontend

- React 18 with TypeScript
- Vite build tool
- React Router for navigation
- Axios for API communication
- CSS Modules for styling

See [frontend/README.md](frontend/README.md) for setup instructions.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Configure .env with your PostgreSQL credentials
flask db upgrade
flask run
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Configure VITE_API_BASE_URL if needed
npm run dev
```
