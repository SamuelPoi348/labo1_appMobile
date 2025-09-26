from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField, TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
import sqlalchemy as sa
from app.models import Utilisateur
from app import db


class FormConnexion(FlaskForm):
   nom_utilisateur = StringField("Nom utilisateur ",validators=[DataRequired(message="Le nom d'utilisateur est requis.")])
   mot_passe = PasswordField("Password",validators=[DataRequired(message="Le mot de passe est requis.")])
   se_souvenir = BooleanField("Se souvenir de moi ")
   connexion_submit = SubmitField("se connecter")
    
class FormEnregistrement(FlaskForm):
   nom_utilisateur = StringField("Nom utilisateur ",
            validators=[DataRequired(message="Le nom d'utilisateur est requis."),
            Length(min=4, max=25, message="Le nom d'utilisateur doit être entre 4 et 25 caractères.")])
   email = StringField("Email ",
            validators=[DataRequired(message="L'email est requis."),
                        Email(message="Adresse email invalide.")])
   mot_passe = PasswordField("Password",
            validators=[DataRequired(message="Le mot de passe est requis."),
                        Length(min=6, message="Le mot de passe doit contenir au moins 6 caractères.")])
   mot_passe2 = PasswordField("Confirmer Password",
            validators=[DataRequired(message="La confirmation du mot de passe est requise."),
                        EqualTo('mot_passe', message="Les mots de passe doivent correspondre.")])
   
   soumettre = SubmitField("Enregistrer")

   def validate_nom_utilisateur(self, nom_utilisateur):
          utilisateur = db.session.scalar(sa.select(Utilisateur).where(Utilisateur.nom_utilisateur == nom_utilisateur.data))
          if utilisateur is not None:
              raise ValidationError('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

      # Validateur personnalisé pour l'unicité de l'email
   def validate_email(self, email):
          utilisateur = db.session.scalar(sa.select(Utilisateur).where(Utilisateur.email == email.data))
          if utilisateur is not None:
              raise ValidationError('Cet email est déjà utilisé. Veuillez en choisir un autre.')

class FormEditionProfil(FlaskForm):
    nom_utilisateur = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=2, max=64)])
    a_propos_moi = TextAreaField('À propos de moi', validators=[Length(max=140)])
    submit = SubmitField('Enregistrer')


