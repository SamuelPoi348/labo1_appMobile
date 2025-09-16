from flask import Flask
from app import app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin

# Config de Flask Login
login = LoginManager(app)
login.login_view = 'connexion' # Nom de la vue pour la page de connexion
login.login_message = 'Veuillez vous connecter pour accéder à cette page.'

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

from app import routes

