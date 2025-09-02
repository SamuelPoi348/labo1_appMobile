from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired

class FormConnexion:
    nom_utilisateur = StringField("Nom utilisateur ",validators=[DataRequired()])
    mot_passe = PasswordField("Password",validators=[DataRequired()])
    se_souvenir = BooleanField("Se souvenir de moi ")
    connexion_submit = SubmitField("se connecter")