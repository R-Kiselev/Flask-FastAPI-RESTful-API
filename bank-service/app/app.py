from flask import Flask

from app import api
from app import auth
from app import flask_cli
from app.error_handling import register_app_errorhandlers
from app.extensions import db, migrate, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")

    configure_extensions(app)
    configure_cli(app)
    register_app_errorhandlers(app)
    register_blueprints(app)

    return app


def configure_cli(app):
    app.cli.add_command(flask_cli.init)


def configure_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)
