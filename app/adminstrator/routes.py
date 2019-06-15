import json
import os
from datetime import datetime
from secrets import token_urlsafe, randbits
import requests
from flask import render_template, flash, redirect, url_for, request, \
    g, current_app, json, send_from_directory, jsonify,abort
from flask_babel import _, get_locale
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_required
from app import db
from app.adminstrator import bp
from app.models import User, Applicant, Permission, Role
from .. import mqtt
from .. import socketio
import cloudinary
import cloudinary.api
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import pycountry


# TODO: Account Route

cloudinary.config(
    cloud_name='intelecs',
    api_key='815186897625597',
    api_secret='u0IjmaHsoWvyHbuFpoYtCYmL61U'
)

@bp.before_request
def before_request():
    role = Role.query.filter_by(user_id=current_user.id).first()
    if role.name != Permission.ADMIN:
        flash("Sorry!, you cant access this page!.")
        return redirect(url_for('main.index'))

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('admin/index.html', title=_('Dashbooard'))


@bp.route('/applications')
@login_required
def applications():
    applicants = Applicant.query.all()

    return render_template('admin/applicants.html', applicants=applicants, title=_('Applicant'))

@bp.route('/applicant/<string:token>')
@login_required
def applicant(token):
    applicant = Applicant.query.filter_by(secure_token=token).first()
    if applicant is None:
        return 'This applicant does not exist'
    return render_template('admin/applicant.html', applicant=applicant, title=_(applicant.full_name))




@bp.route('/approve_applicant/<token>')
@login_required
def approve(token):
    applicant = Applicant.query.filter_by(secure_token=token).first()
    if applicant is None: abort(404)


    if applicant.email_confirmed:
        applicant.registration_id =randbits(32)
        applicant.set_accepted()
        db.session.commit()
        return redirect(url_for('administrator.applicant', token=applicant.secure_token))
    flash("Email not confirmed cant approve this use")
    return redirect(url_for('administrator.applicants'))

@bp.route('/disapprove/<string:token>')
@login_required
def disapprove(token):
    applicant = Applicant.query.filter_by(secure_token=token).first()
    if applicant is None: abort(404)

    applicant.un_accept()
    flash("This applicant is No longer accepted as Baby sitter")


@bp.route('/account/<string:username>/<string:token>')
@login_required
def account(username, token):
    user = User.query.filter_by(username=username).first()

    if user is None: abort(404)

    if user.secure_token == token:
        return render_template('admin/user.html', user=user, title=_(user.username))

    return 'Some thing not okay'

@bp.route('/messages')
@login_required
def messages():
    pass

@bp.route('/message/<string:token>')
@login_required
def message(token):
    pass

@bp.route('/new-message/')
@login_required
def new_message():
    pass



