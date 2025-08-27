from flask import Flask
from app.config import Config
from app.database import db
from app.routes.ask import ask_bp
from app.routes.purchase import purchase_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init db
    db.init_app(app)
    with app.app_context():
        from app import models  # ensure models are registered
        db.create_all()

    # register blueprints
    app.register_blueprint(ask_bp)
    app.register_blueprint(purchase_bp)

    @app.route('/health', methods=['GET'])
    def health():
        return {"status": "ok"}, 200

    return app
