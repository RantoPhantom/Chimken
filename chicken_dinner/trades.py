import functools
from flask import (Blueprint, render_template, request, url_for)

bp = Blueprint('trades', __name__, url_prefix='/trades')


@bp.route('/')
def trade():
    return render_template('trades/trades.html')
