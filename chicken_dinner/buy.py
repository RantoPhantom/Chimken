import functools
from flask import (Blueprint, render_template, request, url_for)

bp = Blueprint('buy', __name__, url_prefix='/buy')


@bp.route('/')
def trade():
    return render_template('buy/buy.html', style="styles.css")
