import functools
from flask import (Blueprint, render_template, request, url_for, g)
from .auth import login_required

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index/index.html', g=g)
