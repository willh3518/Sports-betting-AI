from flask import Flask

def create_app():
    app = Flask(__name__)
    from .routes.routes import main_routes  # Ensure this path matches where your Blueprint is defined
    app.register_blueprint(main_routes)

    return app
