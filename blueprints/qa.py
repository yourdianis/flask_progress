from flask import Blueprint

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    return "QA Index Page"


@bp.route('/public_qa')
def public_qa():
    return "Public QA Page"


@bp.route('/search')
def search():
    return "Search Page"