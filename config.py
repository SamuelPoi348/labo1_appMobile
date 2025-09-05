import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une_clé_secrète_par_défaut'