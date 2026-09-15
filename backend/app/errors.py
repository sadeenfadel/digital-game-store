import logging
from flask import jsonify
from marshmallow import ValidationError

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        message = getattr(error, "description", str(error))
        return jsonify({"error": {"code": "BAD_REQUEST", "message": message}}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        message = getattr(error, "description", str(error))
        return jsonify({"error": {"code": "UNAUTHORIZED", "message": message}}), 401

    @app.errorhandler(403)
    def forbidden(error):
        message = getattr(error, "description", str(error))
        return jsonify({"error": {"code": "FORBIDDEN", "message": message}}), 403

    @app.errorhandler(404)
    def not_found(error):
        message = getattr(error, "description", str(error))
        return jsonify({"error": {"code": "NOT_FOUND", "message": message}}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"error": {"code": "UNPROCESSABLE", "message": "Validation error."}}), 422

    @app.errorhandler(500)
    def internal_error(error):
        logger.exception("Internal server error")
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred."}}), 500

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": str(error.messages)}}), 400
