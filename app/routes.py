from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
# ajouter le code pour la route
# utiliser render_template pour faire afficher la page html
# faire passer les données nécessaires au template
    return render_template('index.html')