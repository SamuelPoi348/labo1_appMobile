from app import app
from flask import render_template, redirect, url_for, flash, session
from app.form import FormConnexion  
from app.models import Utilisateur, Post

utilisateur = "Samuel Poirier"
critiques = [ 
    {
        "nom_utilisateur": "FilmLover23",
        "film": "Oppenheimer",
        "commentaire": "Un chef-d'œuvre cinématographique ! Nolan nous livre une biographie captivante avec des performances exceptionnelles."
    },
    {
        "nom_utilisateur": "CinéPassionné",
        "film": "Spider-Man: Across the Spider-Verse",
        "commentaire": "L'animation est révolutionnaire et l'histoire multi-dimensionnelle est brillamment exécutée."
    },
    {
        "nom_utilisateur": "MovieCritic2024",
        "film": "The Batman",
        "commentaire": "Une approche sombre et mature du personnage. Robert Pattinson surprend dans le rôle titre."
    },
    {
        "nom_utilisateur": "FilmExpert",
        "film": "Dune",
        "commentaire": "Adaptation fidèle et visuellement époustouflante. Denis Villeneuve maîtrise parfaitement l'univers de Herbert."
    }
]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', critiques=critiques, utilisateur=utilisateur)

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form = FormConnexion()
    if form.validate_on_submit():
        session['nom_utilisateur'] = form.nom_utilisateur.data
        session['se_souvenir'] = form.se_souvenir.data
        if session['nom_utilisateur'] =="admin" and form.mot_passe.data == "admin":
            flash(f'Bienvenue {form.nom_utilisateur.data}, remember_me={form.se_souvenir.data}', 'success')
        else :
            flash(f'Connexion requise pour acceder à cette page {form.nom_utilisateur.data}, remember_me={form.se_souvenir.data}', 'error')

        return redirect(url_for('index'))  
    return render_template('connexion.html', form=form)
