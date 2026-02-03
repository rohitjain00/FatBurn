from flask import Flask
from flask_session import Session
from config import Config
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    db.init_app(app)
    Session(app)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Ensure database is created
    with app.app_context():
        db.create_all()

    return app
