import functools
from flask import (Blueprint, render_template, request, url_for)
from .auth import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
@login_required
def index():
    return render_template('profile/profile.html')
