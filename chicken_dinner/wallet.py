import functools
from flask import (Blueprint, render_template, request, url_for)

bp = Blueprint('wallet', __name__, url_prefix='/wallet')


@bp.route('/')
def index():
    return render_template('wallet/wallet.html')
