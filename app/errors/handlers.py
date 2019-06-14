from flask import render_template, request
from flask_login import current_user
from app import db
from app.errors import bp
from flask_babel import _


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', title=_('Not Found')), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html', title=_('Internal Error')), 500