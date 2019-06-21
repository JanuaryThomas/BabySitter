import json
import os
from datetime import datetime
import geocoder

import requests
from secrets import token_urlsafe
from flask import render_template, flash, redirect, url_for, request, \
    g, current_app, json, send_from_directory, jsonify, abort
from flask_babel import _, get_locale
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import User, BillingAddress, Location, BabySitter, BabySitterSelection, Parent, Notification, BabysitterNotification
from .. import mqtt
from .. import socketio
import requests
import pesapal
from app.main.forms import EditProfileForm, EditBillingAddressForm, BillingAddressForm, ProfileForm, PhoneForm


PESA_PAL_CONSUMER = 'IU5LNHtKJZSJjj3fLsV1iQKRIxnkzOFY'
PESA_PAL_SECRECT = 'jM2GRNgzUjgJcKthv2l6yoChP+A='

pesapal.consumer_key = PESA_PAL_CONSUMER
pesapal.consumer_secret = PESA_PAL_SECRECT
pesapal.testing = False

post_params = {
    'oauth_callback' : 'https://google.com'
}

@bp.before_request
def before_request():
    pass


@bp.route('/locs')
def locs():
    data = {
        "rest": []
    }
    for location in Location.query.all():
        lats = []
        lats.append(location.user_lng)
        lats.append(location.user_lat)
        data["rest"].append(lats)
    return jsonify(data)

@bp.route('/')
@bp.route('/index')
@bp.route('/landing')
def landing():
    # if current user is authenticated redirect to current page
    return render_template('landing/index.html', title=_('Home'))

@bp.route('/parent')
@login_required
def index():
    if current_user.first_name is None:
        if current_user.last_name is None:
            return redirect(url_for('main.profile', token=current_user.secure_token))
    locations = Location.query.all()
    baby_siters = BabySitter.query.all()

    user_lat = 0.0
    user_lng = 0.0

    try:
        g = geocoder.ip("me")

        user_lat = g.latlng[0]
        user_lng = g.latlng[1]
    except Exception as e:
        flash("Error accessing your location, check your Internet or GPS")
    data = {}

    for location in locations:
        for baby_siter in baby_siters:
            if baby_siter.user_id == location.user_id:
                if location.user.is_available:
                    data.update(
                        {
                            'type': 'Feature',
                            'geometry': {
                                'type': 'Point',
                                'coordinates': [location.user_lng, location.user_lat]
                            },
                            'properties': {
                                'profile': str(location.user.profile_pic),
                                'title': (location.user.username),
                                'phone': str(location.user.phone),
                                "token" : str(baby_siter.secure_token)
                            }
                        }
                    )

    return render_template('main/index.html', title=_('Home'), data=data, user_lat=user_lat, user_lng=user_lng)


@bp.route('/profile/<string:token>',  methods=['GET', 'POST'])
def profile(token):
    user = User.query.filter_by(secure_token=token).first()
    if user is None: abort(404)

    form = ProfileForm()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.gender = form.gender.data
        user.age = form.date_of_birth.data
        db.session.commit()
        flash('Profile has been updated! ')
        return redirect(url_for('main.index'))

    form.first_name.data = user.first_name
    form.gender.data = user.gender
    form.date_of_birth.data = user.age
    return render_template('main/complete_profile.html', form=form, title=_('Complete Profile'))


@bp.route('/messages/<string:token>')
@login_required
def messages(token):
    pass

@bp.route('/account/<string:token>')
@login_required
def account(token):
    pass

@bp.route('/add-billing/<string:token>', methods=['GET', 'POST'])
def add_billing(token):
    form = BillingAddressForm()

    user = User.query.filter_by(secure_token=token).first()

    if user is None:
        abort(404)

    if form.validate_on_submit():
        billing = BillingAddress(
            user_id=current_user.id,
            address_line_1=form.address_line_1.data,
            address_line=form.address_line.data,
            town=form.town.data,
            State=form.state.data,
            zip_code=form.zip_code.data
        )

        db.session.add(billing)
        db.session.commit()
        flash('Your Billing Address has Been Added')
        return redirect(url_for('main.index'))


    return render_template('main/add_billing.html', form=form, title=_('Add Billing'))


@bp.route('/add-phone', methods=["POST", "GET"])
@login_required
def add_phone():
    form = PhoneForm()
    if form.validate_on_submit():
        current_user.phone = form.phone.data
        db.session.commit()
        flash("Phone Number has been added")
        return redirect(url_for('main.index'))
    return render_template('main/add-phone.html', title=('Add Phone Number'), form=form)


@bp.route('/edit-billing/<string:token>', methods=['GET', 'POST'])
def edit_billing(token):
    form = EditBillingAddressForm()

    user = User.query.filter_by(secure_token=token).first()

    if user is None:
        abort(404)
    billing = BillingAddress.query.filter_by(user_id=user.id).first()

    if form.validate_on_submit():
        billing.address_line_1 = form.address_line_1.data
        billing.address_line = form.address_line.data
        billing.town = form.town.data
        billing.State = form.state.data
        billing.zip_code = form.zip_code.data

        db.session.commit()
        flash('Your Billing Address has Been Updated')

    return render_template('main/edit_billing.html', form=form, title=_('Edit Billing'))


@bp.route('/add-credit-card/<string:token>')
def add_credit_card(token):
    pass

@socketio.on('selection_accept')
def handle_accept(json_str):
    print(json_str)


# Complete Booking
@bp.route('/complete-sitting/<string:token>')
def complete(token):
    pass

@bp.route('/select-baby-sitter/<string:token>')
def select_baby_sitter(token):
    baby_sitter = BabySitter.query.filter_by(secure_token=token).first()
    parent = Parent.query.filter_by(user_id=current_user.id).first()
    selections = BabySitterSelection.query.all()
    if baby_sitter is None: abort(404)

    for selection in selections:
        if selection is None:
            flash("You dont have any selections")
            return redirect(url_for('main.index'))
        if selection.baby_sitter_id == baby_sitter.id and selection.parent_id == parent.id:
                flash("You have already selected this baby Sitter")
                return redirect(url_for('main.selection'))
        elif selection.baby_sitter_id == baby_sitter.id:
            flash("This baby sitter is occupied")
            return redirect(url_for('main.index'))

    selection = BabySitterSelection(
        baby_sitter_id=baby_sitter.id,
        parent_id=parent.id,
        secure_token=token_urlsafe(16)
    )

    baby_sitter_notification = BabysitterNotification(
        baby_sitter_id=baby_sitter.id,
        secure_token=token_urlsafe(16),
        body="You have new baby Sitting request"
    )
    db.session.add(baby_sitter_notification)
    notification = Notification(
        user_id=current_user.id,
        secure_token=token_urlsafe(16),
        body="New Request has been Sent to",
        notification_id=baby_sitter_notification.id
    )
    db.session.add(notification)
    db.session.commit()
    flash("New Selection has been Sent!")

    db.session.add(selection)
    db.session.commit()

    socketio.emit('selected', {'msg': current_user.username + _(' would like you to baby sit their kid')})

    #TODO : Socket IO and Notificaiton
    return redirect(url_for('main.selection'))

@bp.route('/selection')
def selection():
    parent = Parent.query.filter_by(user_id=current_user.id).first()
    selection = BabySitterSelection.query.filter_by(parent_id=parent.id).first()


    if selection is not None:
        baby_sitter = BabySitter.query.filter_by(id=selection.baby_sitter_id).first()
        user = User.query.filter_by(id=baby_sitter.user_id).first()
        return render_template('main/baby-sitter.html', user=user, selection=selection, title=_('Selection'))
    flash ("You dont have any Baby Sitter selection yet!...")
    return redirect(url_for('main.index'))

@bp.route('/cancel-selection/<string:token>')
def cancel_selection(token):
    baby_sitter = BabySitter.query.filter_by(secure_token=token).first()
    parent = Parent.query.filter_by(user_id=current_user.id).first()
    selection = BabySitterSelection.query.filter_by(baby_sitter_id=baby_sitter.id).first()

    if selection is None: abort(404)
    if selection.parent_id != parent.id:
        flash("You cant delete this selection")
        return redirect(url_for('main.selection'))

    db.session.delete(selection)
    db.session.commit()
    flash("This Selection has been canceled")
    return redirect(url_for('main.index'))

@bp.route('/pay')
def pay():
    return render_template('main/pay.html')


@bp.route('/complete')
def complete_pay():
    return 'Success'




@bp.route('/checkout')
def checkout():
    post_params = {
        'oauth_callback' : url_for('main.complete_pay')
    }

    request_data = {
        'Amount' : '500',
        'Description' : ' Baby Sitter Payment',
        'Type': 'MERCHANT',
        'Reference': token_urlsafe(8),
        'PhoneNumber': current_user.phone
    }

    url = pesapal.postDirectOrder(post_params, request_data)
    response = requests.get(url)
    print(response.content)
    return response.content