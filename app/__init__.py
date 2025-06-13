from flask import Flask
from config import Config # Import your main config

# Initialize Flask extensions here if you use any, e.g.:
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Load instance config if it exists (for secrets not in version control)
    try:
        app.config.from_pyfile('config.py', silent=True)
    except FileNotFoundError:
        # This means instance/config.py does not exist. That's fine for dev,
        # but in production, you'd want it to exist.
        print("Warning: instance/config.py not found. Ensure it's set up for production.")
        pass # Or handle specific errors if needed

    # Initialize extensions with the app instance
    # db.init_app(app)

    # Register Blueprints
    from app.routes.get_ai_response import ai_bp # If you create one

    app.register_blueprint(ai_bp)

    # Example of a simple route for testing the app creation
    @app.route('/')
    def index():
        return "AI Welcomes You."

    return app