from flask import (Blueprint, render_template)

bp = Blueprint('create', __name__, url_prefix='/create')


@bp.route("/")
def index():
    return render_template('create/create.html')
