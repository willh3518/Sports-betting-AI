from flask import Flask
from app.models import db  # ✅ Clarify import path if needed!

def create_app():
    app = Flask(__name__)

    # Import and register blueprints/routes
    from app.routes.routes import main_routes
    app.register_blueprint(main_routes)

    return app
