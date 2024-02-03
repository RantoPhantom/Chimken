import functools
from flask import (Blueprint, render_template, request, url_for)

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index/index.html', name="Quoc an lon")
