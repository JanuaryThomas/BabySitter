import json
import os
from datetime import datetime
from secrets import token_urlsafe
import requests
from flask import render_template, flash, redirect, url_for, request, \
    g, current_app, json, send_from_directory, jsonify, abort, session
from flask_babel import _, get_locale
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_required
from app import db

from app.application import bp
from app.models import User, Applicant, ApplicantID
from .. import mqtt
from .. import socketio
import cloudinary
from app.application.forms import BabySitterApplicationForm, RequestPasswordForm, LoginForm, \
    BabySitterUpdateForm
import cloudinary.api
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import pycountry
from app.application.email_auth import send_confirm_email, send_temp_password


cloudinary.config(
    cloud_name='intelecs',
    api_key='815186897625597',
    api_secret='u0IjmaHsoWvyHbuFpoYtCYmL61U'
)


@bp.before_request
def before_request():
    pass

@bp.route('/home')
@bp.route('/index')
@bp.route('/')
def index():
    return render_template('application/index.html', title=_('Home'))

@bp.route('/apply', methods=['GET', 'POST'])
def apply():
    form = BabySitterApplicationForm()

    if form.validate_on_submit():
        upload_result = upload(form.id_document.data)

        applicant = Applicant(
            full_name=form.full_name.data,

            email=form.email.data,
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            secure_token=token_urlsafe(16)
        )

        db.session.add(applicant)
        db.session.commit()

        applicant_id = ApplicantID(
            applicant_id=applicant.id,
            secure_token=token_urlsafe(16),
            url=upload_result['url']
        )

        db.session.add(applicant_id)
        db.session.commit()
        flash("Check your inbox new email has been sent!")
        return redirect(url_for('application.resend_confirm', email=applicant.email))

    return render_template('application/application.html', form=form, title='Apply')

@bp.route('/unconfirmed/<string:email>')
def unconfirmed(email):
    applicant = Applicant.query.filter_by(email=email).first()

    if applicant is None:
        abort(404)
    if applicant.email_confirmed:
        return render_template('application/email_confirmed.html', title=_('Email Confirmed'))
    return redirect(url_for('application.resend_confirm', email=applicant.email))

@bp.route('/confirm/<string:email>/<string:token>')
def confirm(token, email):
    applicant = Applicant.query.filter_by(email=email).first()

    if applicant is None:
        abort(404)
    if applicant.confirm(token):
        return render_template('application/email_confirmed.html', title=_('Email Confirmed'))
    else:
        print('The link is invalid')
    return render_template('application/confirm.html', title=_('Confirm your email'))

@bp.route('/send_confirm/<string:email>')
def resend_confirm(email):
    applicant = Applicant.query.filter_by(email=email).first()

    if applicant is None:
        abort(404)
    if applicant.email_confirmed:
        return render_template('application/email_confirmed.html', title=_('Email Confirmed'))
    token = applicant.generate_confirmation_token()
    send_confirm_email(applicant, token)
    return render_template('application/sent_confirm_email.html', title=_('Email Sent'), applicant=applicant)

@bp.route('/get_password', methods=['GET', 'POST'])
def get_password():
    form = RequestPasswordForm()


    if form.validate_on_submit():
        applicant = Applicant.query.filter_by(email=form.email.data).first()
        if applicant is None:
            abort(404)


        token = token_urlsafe(6)
        send_temp_password(applicant, token)

        applicant.token = token
        db.session.commit()
        flash('Password token as been sent to your email')

        return render_template('application/token_sent.html', title=_('Token Sent! '))

    return render_template('application/password_request_form.html', form=form, title=_('Request PIN'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        applicant = Applicant.query.filter_by(email=form.email.data).first()

        if applicant is None:
            abort(404)

        if applicant.token == form.password.data:
            session['logged_in'] = True
            session['email'] = applicant.email

        return redirect(url_for('application.account'))
    return render_template('application/login.html', form=form, title='Log in')

@bp.route('/account')
def account():
    if not session['logged_in']:
        return redirect(url_for('application.login'))
    applicant = Applicant.query.filter_by(email=session['email']).first()

    if applicant is None:
        return render_template('application/applicant_login.html')

    return render_template('application/account.html', title=applicant.first_name, applicant=applicant)

@bp.route('/edit_account/<string:email>', methods=['GET', 'POST'])
def edit_profile(email):
    if not session['logged_in']:
        return redirect(url_for('application.login'))
    applicant = Applicant.query.filter_by(email=email).first()
    form = BabySitterUpdateForm()
    if session['email'] == applicant.email:

        if form.validate_on_submit():
            upload_result = upload(form.id_document.data)

            applicant.first_name = form.first_name.data
            applicant.last_name = form.last_name.data
            applicant.email = form.email.data
            applicant.gender = form.gender.data
            applicant.date_of_birth = form.date_of_birth.data
            applicant.secure_token = token_urlsafe(16)
            applicant.email_confirmed = False

            db.session.commit()

            applicant_id = ApplicantID.query.filter_by(applicant_id=applicant.id).first()
            applicant_id.url = upload_result['url']
            db.session.commit()
            return redirect(url_for('application.resend_confirm', email=applicant.email))
        form.first_name.data = applicant.first_name
        form.last_name.data = applicant.last_name
        form.email.data = applicant.email
        return render_template('application/edit_account.html', form=form, title=_('Edit Account'))
    return redirect(url_for('application.get_password'))