from flask import Blueprint

bp = Blueprint('application', __name__)

from app.application import routes