from flask import Blueprint
from app import csrf

bp = Blueprint('babysitter', __name__)
csrf.exempt(bp)

from app.babysitter import routes