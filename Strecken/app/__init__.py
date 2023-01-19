from os import path

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_login import LoginManager



db = SQLAlchemy()
DB_NAME = "database.db"
marsh = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'juliaHammer'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    marsh.init_app(app)

    from .view import view
    from .authentifikation import auth

    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .api import api
    from .models import Mitarbeiter, BahnhofModel, AbschnittModel, StreckenModel, abschnitt

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    app.register_blueprint(api, url_prefix="/")

    @login_manager.user_loader
    def load_user(id):
        return Mitarbeiter.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Datenbank erstellt!')
