import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une_clé_secrète_par_défaut'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  

     # Configuration email (Gmail par exemple)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'one@gamil.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'mot_de_passe_ou_app_password'
    MAIL_DEFAULT_SENDER = ('LaboApp', MAIL_USERNAME)
    ADMINS = ['one@gamil.com']
    POSTS_PER_PAGE = 3