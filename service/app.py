from flask import Flask
from service.models import db
from service.routes import register_routes

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///products.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    register_routes(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()
