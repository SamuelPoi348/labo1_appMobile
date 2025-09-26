from app import app
from flask import render_template, redirect, url_for, flash, session, request
from app.form import FormConnexion  
from app.models import Utilisateur, Post
from flask_login import current_user, login_user, logout_user, login_required
from app.form import FormConnexion, FormEnregistrement
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
from datetime import datetime, timezone



#utilisateur = "Samuel Poirier"
@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.derniere_connexion = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        posts = db.session.scalars(
            sa.select(Post)
              .where(Post.id_utilisateur == current_user.id)
              .order_by(Post.timestamp.desc())
        ).all()
        return render_template('index.html', utilisateur=current_user, posts=posts)
    return render_template('index.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
            return redirect(url_for('index'))
        
    form = FormConnexion()
    if form.validate_on_submit():
          # Recherche de l'utilisateur par nom d'utilisateur
          utilisateur = db.session.scalar(
              sa.select(Utilisateur).where(Utilisateur.nom_utilisateur == form.nom_utilisateur.data)
          )

          # Vérification du mot de passe avec la méthode verifier_mot_de_passe()
          if utilisateur is None or not utilisateur.verifier_mot_de_passe(form.mot_passe.data):
              flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
              return redirect(url_for('connexion'))


          # Créer la session utilisateur et gérer "Se souvenir de moi"
          login_user(utilisateur, remember=form.se_souvenir.data)

          


          # Gestion de la redirection après connexion (paramètre next)
          page_suivante = request.args.get('next')
          if not page_suivante or urlsplit(page_suivante).netloc != '':
             page_suivante = url_for('profil', nom_utilisateur=utilisateur.nom_utilisateur)
          return redirect(page_suivante)

    return render_template('connexion.html', form=form)

@app.route('/deconnexion')
def deconnexion():
    logout_user()
    return redirect(url_for('index'))


@app.route('/enregistrement', methods=['GET', 'POST'])
def enregistrement():
      # Rediriger vers index si l'utilisateur est déjà connecté
      if current_user.is_authenticated:
          return redirect(url_for('index'))

      # Créer une instance de FormEnregistrement
      form = FormEnregistrement()

      # Vérifier si le formulaire est valide avec validate_on_submit()
      if form.validate_on_submit():
          # Instancier un objet Utilisateur avec les données du formulaire
          utilisateur = Utilisateur(nom_utilisateur=form.nom_utilisateur.data, email=form.email.data # type: ignore
          )

          # Appeler la méthode genere_mot_passe() avec le mot de passe du formulaire
          utilisateur.genere_mot_passe(form.mot_passe.data)

          # Ajouter l'utilisateur à la session de base de données
          db.session.add(utilisateur)

          # Effectuer le commit
          db.session.commit()

          # Afficher un message flash de confirmation
          flash('Félicitations, vous êtes maintenant enregistré!', 'success')

          # Rediriger vers la page de connexion
          return redirect(url_for('connexion'))

      # Sur un GET: Rendre le template form_enregistrement.html avec le formulaire
      return render_template('enregistrement.html', form=form)

@app.route('/user/<nom_utilisateur>')
@login_required
def profil(nom_utilisateur):
    utilisateur = db.session.scalar(
        sa.select(Utilisateur).where(Utilisateur.nom_utilisateur == nom_utilisateur)
    )
    if utilisateur is None:
        flash(f"L'utilisateur {nom_utilisateur} n'a pas été trouvé.", 'error')
        return redirect(url_for('index'))
    
    posts = db.session.scalars(
        sa.select(Post).where(Post.id_utilisateur == utilisateur.id).order_by(Post.timestamp.desc())
    ).all()
    
    return render_template('user.html', utilisateur=utilisateur, posts=posts)

