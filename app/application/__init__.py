from flask import Blueprint
from app import  csrf
bp = Blueprint('application', __name__)

csrf.exempt(bp)
from app.application import routes