from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from app import db  # <- IMPORTER l'instance db unique, PAS en recréer une
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import hashlib
#fix pour les follow unfollow
from sqlalchemy.orm import Mapped


followers = sa.Table(
    'followers',
    db.Model.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('utilisateur.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('utilisateur.id'),
              primary_key=True)
)

class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'utilisateur'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nom_utilisateur: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, index=True)
    mot_passe_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    a_propos_moi: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    derniere_connexion: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime)
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='auteur')

    def __repr__(self):
        return f'<Utilisateur {self.nom_utilisateur}>'

    def genere_mot_passe(self, mot_de_passe):
        self.mot_passe_hash = generate_password_hash(mot_de_passe)

    def verifier_mot_de_passe(self, mot_de_passe):
        if self.mot_passe_hash is None:
            return False
        return check_password_hash(self.mot_passe_hash, mot_de_passe)
      
    def avatar(self, taille=100):
        digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={taille}"
    
    following: Mapped[list["Utilisateur"]] = so.relationship(
    secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    back_populates='followers'
)
    followers: Mapped[list["Utilisateur"]] = so.relationship(
    secondary=followers,
    primaryjoin=(followers.c.followed_id == id),
    secondaryjoin=(followers.c.follower_id == id),
    back_populates='following'
)
    
    def follow(self, utilisateur):
        if not self.is_following(utilisateur):
            self.following.append(utilisateur)
    
    def unfollow(self, utilisateur):
        if self.is_following(utilisateur):
            self.following.remove(utilisateur)
    
    #def is_following(self, utilisateur):
     #   query = self.following.select().where(Utilisateur.id == utilisateur.id)
      #  return db.session.scalar(query) is not None
    
    def is_following(self, utilisateur):
       return db.session.scalar(
        sa.select(followers)
        .where(
            followers.c.follower_id == self.id,
            followers.c.followed_id == utilisateur.id
        )
    ) is not None

    #def followers_count(self):
    #    query = sa.select(sa.func.count()).select_from(
    #        self.followers.select().subquery())
    #    return db.session.scalar(query)
    
    #def following_count(self):
    #    query = sa.select(sa.func.count()).select_from(
    #        self.following.select().subquery())
    #    return db.session.scalar(query)
    
    def followers_count(self):
      return db.session.scalar(
        sa.select(sa.func.count())
        .select_from(followers)
        .where(followers.c.followed_id == self.id)
    )

    def following_count(self):
      return db.session.scalar(
        sa.select(sa.func.count())
        .select_from(followers)
        .where(followers.c.follower_id == self.id)
    )

    def following_posts(self):
       Author = so.aliased(Utilisateur)
       Follower = so.aliased(followers)
       return (
           sa.select(Post)
           .join(Post.author.of_type(Author))
           .join(Author.followers.of_type(Follower), isouter=True)
           .where(
               sa.or_(
                   Follower.c.follower_id == self.id,
                   Post.id_utilisateur == self.id
               ))
               .group_by(Post)
                .order_by(Post.timestamp.desc())
       )


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    contenu: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        default=datetime.now(tz=timezone.utc),
        nullable=False
    )
    id_utilisateur: so.Mapped[int] = so.mapped_column(sa.ForeignKey('utilisateur.id'), nullable=False)
    auteur: so.Mapped["Utilisateur"] = so.relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post {self.id} par Utilisateur {self.id_utilisateur}>"
