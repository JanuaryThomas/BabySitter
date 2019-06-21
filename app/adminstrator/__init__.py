from flask import Blueprint
from app import csrf

bp = Blueprint('administrator', __name__)
csrf.exempt(bp)


from app.adminstrator import routes