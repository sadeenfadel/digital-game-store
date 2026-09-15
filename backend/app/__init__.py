import logging
from flask import Flask, jsonify
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors
from app.errors import register_error_handlers
from app.docs.openapi import configure_swagger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_smorest_api = None


def create_app(config_name="development"):
    global _smorest_api
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_health_check(app)

    return app


def register_extensions(app):
    global _smorest_api
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    _smorest_api = configure_swagger(app)


def register_blueprints(app):
    from app.api.auth import auth_bp
    from app.api.products import products_bp
    from app.api.orders import orders_bp

    _smorest_api.register_blueprint(auth_bp, url_prefix="/api/auth")
    _smorest_api.register_blueprint(products_bp, url_prefix="/api/products")
    _smorest_api.register_blueprint(orders_bp, url_prefix="/api/orders")


def register_health_check(app):
    @app.route("/health", methods=["GET"])
    def health_check():
        try:
            db.session.execute(db.text("SELECT 1"))
            return jsonify({"status": "ok", "database": "connected"}), 200
        except Exception as e:
            logger.exception("Health check failed")
            return jsonify({"status": "error", "database": "disconnected"}), 503
