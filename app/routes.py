from app import app
from flask import render_template
utilisateur = "Samuel Poirier"
critiques = [ 
{ 
"nom_utilisateur": "FilmLover23", "film": "Oppenheimer", 
"commentaire": "Un chef-d'œuvre cinématographique ! Nolan nous livre une biographie captivante avec des performances exceptionnelles." 
}, 
{ 
"nom_utilisateur": "CinéPassionné", "film": "Spider-Man: Across the Spider-Verse", 
"commentaire": "L'animation est révolutionnaire et l'histoire multi-dimensionnelle est brillamment exécutée." 
}, 
{ 
"nom_utilisateur": "MovieCritic2024", "film": "The Batman", 
"commentaire": "Une approche sombre et mature du personnage. Robert Pattinson surprend dans le rôle titre." 
}, 
{ 
"nom_utilisateur": "FilmExpert", "film": "Dune", 
"commentaire": "Adaptation fidèle et visuellement époustouflante. Denis Villeneuve maîtrise parfaitement l'univers de Herbert." 
} 
] 

@app.route('/')
@app.route('/index')
def index():
# ajouter le code pour la route
# utiliser render_template pour faire afficher la page html
# faire passer les données nécessaires au template
    return render_template('index.html',critiques=critiques,utilisateur=utilisateur)