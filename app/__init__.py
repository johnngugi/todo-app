from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_oauth import OAuth
from config import config

db = SQLAlchemy()
lm = LoginManager()
oauth = OAuth()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    lm.init_app(app)
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    with app.app_context():
        db.create_all()
    return app
