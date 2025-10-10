from flask import Flask
#from app import app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
import logging
from logging.handlers import SMTPHandler
#from app.models import Utilisateur, Post

# Config de Flask Login
app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'connexion' # Nom de la vue pour la page de connexion
login.login_message = 'Veuillez vous connecter pour accéder à cette page.'


app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login.login_view = 'connexion'

login.login_message = 'Veuillez vous connecter pour accéder à cette page.'


if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Labo01_1 Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        
from app import models

from app import routes

from app.models import Utilisateur

from app import errors


@login.user_loader
def load_user(id):
    return db.session.get(Utilisateur, int(id))


    

