from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired


class FormConnexion(FlaskForm):
   nom_utilisateur = StringField("Nom utilisateur ",validators=[DataRequired(message="Le nom d'utilisateur est requis.")])
   mot_passe = PasswordField("Password",validators=[DataRequired(message="Le mot de passe est requis.")])
   se_souvenir = BooleanField("Se souvenir de moi ")
   connexion_submit = SubmitField("se connecter")
    
