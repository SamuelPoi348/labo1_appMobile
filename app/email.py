from flask import render_template
from app import app
from flask_mail import Message
from app import mail


def send_password_reset_email(utilisateur):
    token = utilisateur.get_reset_password_token()
    send_email('[Microblog] Réinitialisation de mot de passe', 
                sender=app.config['ADMINS'][0],
                recipients=[utilisateur.email],
                text_body=render_template('email/reset_password.txt',
                                           utilisateur=utilisateur, token=token),
                html_body=render_template('email/reset_password.html',
                                           utilisateur=utilisateur,token=token))

def send_email(subject,sender,recipients,text_body,html_body):
    msg = Message(subject,sender=sender,recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)