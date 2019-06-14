from flask import Blueprint

bp = Blueprint('babysitter', __name__)

from app.babysitter import routes