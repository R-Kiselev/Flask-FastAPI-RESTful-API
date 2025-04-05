import os
import logging

from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.exceptions import HTTPException

from app.extensions import db

ENV = os.getenv('FLASK_ENV', 'production').lower()

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
log_dir = os.path.dirname(__file__)
handler = logging.FileHandler(f"{os.path.join(log_dir, __name__)}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def handle_validation_error(e):
    logger.error(f"Validation Error: {str(e)}")
    return jsonify({"error_type": "Validation Error", "error_message": e.messages}), 400


def handle_database_integrity_error(e):
    db.session.rollback()
    logger.error(f"Database Integrity Error: {str(e)}")

    if ENV == 'development':
        return jsonify({
            "error_type": "Database Integrity error",
            "error_message": str(e)
        }), 500

    if "Duplicate" in str(e):
        error_message = "A conflict occurred. The data you provided already exists."
        status_code = 409
    else:
        error_message = "Please verify your input and try again."
        status_code = 400

    return jsonify({
        "error_type": "Data error",
        "error_message": error_message
    }), status_code


def handle_database_error(e):
    db.session.rollback()
    logger.error(f"Database Error: {str(e)}")
    return jsonify({"error_type": "Database error", "error_message": str(e)}), 500


def handle_http_exception(e):
    logger.error(f"HTTP Error: {str(e)}")
    return jsonify({"error_type": "Http error", "error_message": e.description}), e.code


def handle_general_exception(e):
    logger.error(f"General Error: Type={type(e).__name__}, Message={str(e)}")
    return jsonify({"error_type": type(e).__name__, "error_message": str(e)}), 500


def register_app_errorhandlers(app):
    """Return json errors.

    This will avoid having to try/catch errors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status
    """
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(IntegrityError, handle_database_integrity_error)
    app.register_error_handler(SQLAlchemyError, handle_database_error)
    app.register_error_handler(Exception, handle_general_exception)
