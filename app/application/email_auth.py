from flask import render_template, current_app

from flask_babel import _

from app.email_utility import send_email


def send_confirm_email(user, token):

    send_email(_('Confirm your email'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('application/email/confirm.txt',
                                         user=user, token=token),
               html_body=render_template('application/email/confirm.html',
                                         user=user, token=token))

def send_temp_password(user, token):

    send_email(_('Confirm your email'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('application/email/password.txt',
                                         user=user, token=token),
               html_body=render_template('application/email/password.html',
                                         user=user, token=token))