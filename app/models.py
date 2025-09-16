from typing import Optional, List 
from flask_sqlalchemy import SQLAlchemy 
import sqlalchemy as sa 
import sqlalchemy.orm as so 
from datetime import datetime, timezone, date, time 
import decimal 
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin


db = SQLAlchemy()


#is_authenticated
#is_active
#is_anonymous
#get_id()
#@login.user_loader
#def load_user(id):
# retourner l’utilisateur par son id
class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nom_utilisateur: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=False, unique=True)
    mot_passe_hash: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)

    posts: so.Mapped[List["Post"]] = so.relationship(
        back_populates="utilisateur",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Utilisateur {self.nom_utilisateur}>"
    
    def genere_mot_passe(self, mot_passe: str) -> None:

        self.mot_passe_hash = generate_password_hash(mot_passe)

    def verifier_mot_de_passe(self, mot_passe: str) -> bool:

        return check_password_hash(self.mot_passe_hash,mot_passe)


class Post(db.Model):
    __tablename__ = 'post'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    contenu: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    id_utilisateur: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('utilisateur.id'),
        nullable=False
    )

    utilisateur: so.Mapped["Utilisateur"] = so.relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post {self.id} par Utilisateur {self.id_utilisateur}>"


