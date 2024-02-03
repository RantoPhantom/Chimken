import functools
from flask import (Blueprint, render_template, request, url_for)

bp = Blueprint('market', __name__, url_prefix='/market')


@bp.route('/')
def index():
    return render_template('market/market.html')
