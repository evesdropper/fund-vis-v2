from flask import Flask
# from flask_sqlalchemy import SQLAlchemy


# Globally accessible libraries
# db = SQLAlchemy()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, static_url_path='/static')

    # Initialize Plugins
    # db.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes

        from .src.plot import init_dashboard
        app = init_dashboard(app)

        return app