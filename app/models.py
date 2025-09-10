from typing import Optional, List  
import sqlalchemy as sa 
import sqlalchemy.orm as so 
from datetime import datetime, timezone, date, time 
import decimal 
from app import db


#class NomModele(db.Model):
#    __tablename__ = 'nom_modele'
#
 #   id: so.Mapped[int] = so.mapped_column(primary_key=True)
 #   colonne: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
#
 #   def __repr__(self):
  #      return f'<NomModele {self.colonne}>'