from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import event
app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config["SQLALCHEMY_ECHO"] = True
app.app_context().push()
db = SQLAlchemy(app)
event.listen(db.engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))
migrate = Migrate(app, db,render_as_batch=True)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors