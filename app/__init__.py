# app/__init__.py
from flask import Flask
from .extensions import db, migrate
from .api.profiles import profiles_bp
from .api.queries import queries_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(profiles_bp, url_prefix="/api/v1/profiles")
    app.register_blueprint(queries_bp, url_prefix="/api/v1")

    return app