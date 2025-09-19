from typing import Optional, List 
from flask_sqlalchemy import SQLAlchemy 
import sqlalchemy as sa 
import sqlalchemy.orm as so 
from datetime import datetime, timezone, date, time 
import decimal 
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()


#is_authenticated
#is_active
#is_anonymous
#get_id()
#@login.user_loader
#def load_user(id):
# retourner l’utilisateur par son id
class Utilisateur(db.Model, UserMixin):
      id: so.Mapped[int] = so.mapped_column(primary_key=True)
      nom_utilisateur: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
      email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, index=True)
      mot_passe_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

      posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='auteur')

      def repr(self):
          return f'<Utilisateur {self.nom_utilisateur}>'

      def genere_mot_passe(self, mot_de_passe):
          self.mot_passe_hash = generate_password_hash(mot_de_passe)

      def verifier_mot_de_passe(self, mot_de_passe):
         if self.mot_passe_hash is None:
          return False
         return check_password_hash(self.mot_passe_hash, mot_de_passe)


class Post(db.Model):

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    contenu: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)

    timestamp: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.now(tz=timezone.utc),
        nullable=False
    )
    id_utilisateur: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('utilisateur.id'),
        nullable=False
    )

    auteur: so.Mapped["Utilisateur"] = so.relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post {self.id} par Utilisateur {self.id_utilisateur}>"


