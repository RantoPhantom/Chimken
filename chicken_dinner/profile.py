import functools
from flask import (Blueprint, render_template, request, url_for)

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
def index():
    return render_template('profile/profile.html')
