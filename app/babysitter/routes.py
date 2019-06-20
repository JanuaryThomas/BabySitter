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
from app.babysitter import bp
from app.models import User, Applicant, Permission, Location, BabySitterSelection, Booking, BabySitter, Parent
from .. import socketio
import cloudinary
import cloudinary.api
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import session
import pycountry
import geocoder
from app.babysitter.forms import BabySitterProfileForm, BabySitterAddPhoneForm



cloudinary.config(
    cloud_name='intelecs',
    api_key='815186897625597',
    api_secret='u0IjmaHsoWvyHbuFpoYtCYmL61U'
)

@bp.before_request
def before_request():
    baby_sitter = BabySitter.query.filter_by(user_id=current_user.id).first()
    parrent = Parent.query.filter_by(user_id=current_user.id).first()

    # TODO: UNAUTHORISE VISIT
    if baby_sitter is None:
        pass # Go Home

    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        if current_user.phone is None:
            redirect(url_for('babysitter.add_phone'))

        if current_user.profile_pic is None:
            redirect(url_for('babysitter.profile', token=current_user.secure_token))

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    baby_sitter = BabySitter.query.filter_by(user_id=current_user.id).first()
    if baby_sitter is None: abort(404)
    selection = baby_sitter.baby_sitter_selections


    if selection is None:
        flash("No one has sent you any request!..")
    return render_template('babysitter/index.html', title=_('Home'), selection=selection)

@bp.route('/add-phone', methods=["POST", "GET"])
@login_required
def add_phone():
    form = BabySitterAddPhoneForm()
    if form.validate_on_submit():
        current_user.phone = form.phone.data
        db.session.commit()
        flash("Phone Number has been added")
        return redirect(url_for('babysitter.index'))
    return render_template('babysitter/add_phone.html', title=('Add Phone Number'), form=form)

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


@bp.route('/profile/<string:token>')
@login_required
def profile(token):
    user = User.query.filter_by(secure_token=token).first()
    if user is None:
        abort(404)
    return render_template('babysitter/profile.html', title=_(user.first_name), user=user)

@bp.route('/set-profile', methods=["POST", "GET"])
def set_profile():
    form = BabySitterProfileForm()
    if form.validate_on_submit():
        upload_result = upload(form.id_document.data)
        current_user.profile_pic = upload_result['url']
        db.session.commit()
        flash("Your profile picture has been uploaded")
        return redirect(url_for('babysitter.index'))
    return render_template('babysitter/set_profile.html', form=form)



@bp.route('/set-location', methods=["POST"])
@login_required
def set_location():


    user = User.query.filter_by(secure_token=current_user.secure_token).first()
    if user is None: abort(404)

    location = Location.query.filter_by(user_id=current_user.id).first()
    if location is not None:
        db.session.delete(location)
        db.session.commit()
        flash("Setting up new Location...")
    if request.method == "POST":
        print("Data Received JSON: {}".format(request.get_json()))
        print("Data Received DATA: {}".format(request.get_data()))
        if not request.json: return jsonify({'message': 'Wrong request'})

        lat = request.json["lat"]
        lng = request.json["lng"]
        user.is_available = True
        db.session.commit()
        location = Location(
            user_id=current_user.id,
            user_lat=lat,
            user_lng=lng
        )

        db.session.add(location)
        db.session.commit()
        flash("New Location is set")
        return jsonify({'message': 'Your new Location has been Set'})
    return jsonify({'message': 'error'})



@bp.route('/set-available/')
@login_required
def set_available():
    user = User.query.filter_by(secure_token=current_user.secure_token).first()
    if user is None: abort(404)

    location = Location.query.filter_by(user_id=current_user.id).first()
    if location is not None:
        db.session.delete(location)
        db.session.commit()
    lat = 0.00
    lng = 0.00

    try:
        g = geocoder.ip("me")
        lat = g.latlng[0]
        lng = g.latlng[1]
        user.is_available = True
        db.session.commit()
        location = Location(
            user_id=current_user.id,
            user_lat=lat,
            user_lng=lng
        )

        db.session.add(location)
        db.session.commit()
        flash("You are now available for booking")
    except Exception as e:
        flash("Something went Wrong to access your Location")
    return redirect(url_for('babysitter.index'))

@bp.route('/sample')
@login_required
def sample():
    return render_template('babysitter/sample_base.html')

@bp.route('/selections')
@login_required
def selection():
    baby_sitter = BabySitter.query.filter_by(user_id=current_user.id).first()
    selection = BabySitterSelection.query.filter_by(baby_sitter_id=baby_sitter.id).first()

    return render_template('babysitter/selections.html', selection=selection, title=_('Received selections'))

@bp.route('/accept-order/<string:token>')
@login_required
def accept_order(token):
    pass

@bp.route('/deny-order/<string:token>')
@login_required
def deny_order(token):
    pass

@bp.route('/complete-order/<string:token>')
@login_required
def complete_order(token):
    pass

@bp.route('/booking-history/<string:token>')
@login_required
def booking_history(token):
    pass

@bp.route('/customer-location/<string:token>')
@login_required
def customer_location(token):
    pass