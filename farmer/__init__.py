#from farmer import config_env_files
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_basicauth import BasicAuth


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
basic_auth = BasicAuth(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"


from farmer import views, models
#def prepare_app(environment='development', p_db=db):
    #app.config.from_object(config_env_files[environment])
    #p_db.init_app(app)
    # load views by importing them
    #from . import views
    #return app


def save_and_commit(item):
    db.session.add(item)
    db.session.commit()
db.save = save_and_commit


