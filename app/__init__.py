from flask import Flask
#from app import app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin

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

from app import models

from app import routes

from app.models import Utilisateur


@login.user_loader
def load_user(id):
    return db.session.get(Utilisateur, int(id))

