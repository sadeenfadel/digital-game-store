#!/usr/bin/env python3
"""Seed Demo User for Digital Game Store.

Creates a demo user for testing the API.
Credentials: demo@gamstore.com / password123

Usage:
    cd backend
    python scripts/seed_demo_user.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.extensions import db
from app.services.auth_service import AuthService


def main():
    app = create_app()
    with app.app_context():
        user = AuthService.create_demo_user()
        print(f"\nDemo user ready:")
        print(f"  Email: sadeenfadel@gmail.com")
        print(f"  Password: sAdeen_11")
        print(f"  User ID: {user.id}")


if __name__ == "__main__":
    main()
