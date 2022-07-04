from flask import Flask
# from flask_sqlalchemy import SQLAlchemy


# Globally accessible libraries
# db = SQLAlchemy()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__)  # add config later

    # Initialize Plugins
    # db.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes

        return app
