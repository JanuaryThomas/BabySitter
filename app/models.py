import base64
from datetime import datetime, timedelta
from hashlib import md5
from markdown import markdown
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bleach
import base64
import jwt
import json
import os
from time import time
from flask import current_app, url_for, session
from flask_login import UserMixin, AnonymousUserMixin
from pygments.lexer import default
from werkzeug.security import generate_password_hash, check_password_hash
import redis
import rq
from app import db, login


class Permission:
    BABY_SITTER = '0x01'
    ADMIN = '0x02'
    PARENT = '0x03'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    ward_id = db.Column(db.Integer, db.ForeignKey('wards.id'))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(64), unique=True)
    last_name = db.Column(db.String(64), unique=True)
    secure_token = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(64), unique=True)
    gender = db.Column(db.String(8))
    is_available = db.Column(db.Boolean, default=False)
    age = db.Column(db.DateTime)
    profile_pic = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    approves = db.relationship('ApprovedApplicant', backref='applicant', lazy='dynamic')


    # Basic profile of the user
    role = db.relationship('Role', backref='user', lazy='dynamic')
    locations = db.relationship('Location', backref='user', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    # Parent wise
    billing_address = db.relationship('BillingAddress', backref='parent', lazy='dynamic')
    parent = db.relationship('Parent', backref='parent', lazy='dynamic')

    baby_sitter = db.relationship('BabySitter', backref='baby_sitter', lazy='dynamic')

    # Relational data

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

    def avatar(self, size):
        pass

login.anonymous_user = AnonymousUser

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notification_id = db.Column(db.Integer, db.ForeignKey('baby_sitter_notifications.id'))
    secure_token = db.Column(db.String(128), index=True)
    body = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BabysitterNotification(db.Model):
    __tablename__ = 'baby_sitter_notifications'
    id = db.Column(db.Integer, primary_key=True)
    baby_sitter_id = db.Column(db.Integer, db.ForeignKey('baby_sitters.id'))
    secure_token = db.Column(db.String(128), index=True)
    body = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notifications = db.relationship('Notification', backref='notification', lazy='dynamic')


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    secure_token = db.Column(db.String(128), index=True)
    name = db.Column(db.String(64))

    def set_admin(self):
        self.name = Permission.ADMIN

    def set_parent(self):
        self.name = Permission.PARENT

    def set_baby_sitter(self):
        self.name = Permission.BABY_SITTER

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    secure_token = db.Column(db.String(128), index=True)
    device_size = db.Column(db.String(64))
    user_browser = db.Column(db.String(64))
    user_os = db.Column(db.String(64))
    user_lat = db.Column(db.Float)
    user_lng = db.Column(db.Float)
    user_location = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'user_location': self.user_location,
            'timestamp': self.timestamp
        }
        return data

class BillingAddress(db.Model):
    __tablename__ = 'billing_address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    address_line = db.Column(db.String(120))
    address_line_1 = db.Column(db.String(120))
    secure_token = db.Column(db.String(128), index=True)
    country_id = db.Column(db.Integer)
    town = db.Column(db.String(120))
    State = db.Column(db.String(120))
    zip_code = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'address_line_one': self.address_line_1,
            'address_line_two': self.address_line
        }
        return data

class Parent(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    secure_token = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship('Booking', backref='parent', lazy='dynamic')
    baby_sitter_selections = db.relationship('BabySitterSelection', backref='parent', lazy='dynamic')

class BabySitter(db.Model):
    __tablename__ = 'baby_sitters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    secure_token = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    baby_sitter_selections = db.relationship('BabySitterSelection', backref='baby_sitter', lazy='dynamic')
    booking = db.relationship('Booking', backref='baby_sitter', lazy='dynamic')

class BabySitterSelection(db.Model):
    __tablename__ = 'baby_sitters_selections'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    baby_sitter_id = db.Column(db.Integer, db.ForeignKey('baby_sitters.id'))
    secure_token = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    baby_sitter_id = db.Column(db.Integer, db.ForeignKey('baby_sitters.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    is_confirmed = db.Column(db.Boolean, default=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow())
    end_time = db.Column(db.DateTime, default=datetime.utcnow())
    secure_token = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def confirm(self):
        self.is_confirmed = True


class ApprovedApplicant(db.Model):
    __tablename__ = 'approved_applicants'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Applicant(db.Model):
    __tablename__ = 'applicants'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(120), index=True, unique=True)
    full_name = db.Column(db.String(128))
    secure_token = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(64), unique=True)
    gender = db.Column(db.String(8))
    date_of_birth = db.Column(db.DateTime)
    email_confirmed = db.Column(db.Boolean, default=False)
    accepted = db.Column(db.Boolean, default=False)
    registration_id = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    applicant_ids = db.relationship('ApplicantID', backref='applicant', lazy='dynamic')
    approves = db.relationship('ApprovedApplicant', backref='user', lazy='dynamic')

    available = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            print(token)
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.email_confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def set_accepted(self):
        self.accepted = True

    def un_accept(self):
        if self.accepted:
            self.accepted = False

class ApplicantID(db.Model):
    __tablename__ = 'applicants_ids'
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'))
    secure_token = db.Column(db.String(128), index=True)
    url = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    secure_token = db.Column(db.String(128), index=True)
    name = db.Column(db.String(120))

    regions = db.relationship('Region', backref='country', lazy='dynamic')


class Region(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    secure_token = db.Column(db.String(128), index=True)
    name = db.Column(db.String(120))

    districts = db.relationship('District', backref='region', lazy='dynamic')

class District(db.Model):
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    secure_token = db.Column(db.String(128), index=True)
    name = db.Column(db.String(120))

    wards = db.relationship('Ward', backref='district', lazy='dynamic')

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    secure_token = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    price = db.Column(db.Float, default=0.00)
    bookings = db.relationship('Booking', backref='payment', lazy='dynamic')


class Ward(db.Model):
    __tablename__ = 'wards'
    id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
    secure_token = db.Column(db.String(128), index=True)
    name = db.Column(db.String(120))

    people = db.relationship('User', backref='country', lazy='dynamic')

