from flask import (Blueprint, render_template, g)

bp = Blueprint('create', __name__, url_prefix='/create')


def get_item():
    g.cursor.execute("SELECT * from Users")
    return g.cursor.fetchall()


@bp.route("/")
def index():
    print(get_item())
    return render_template('create/create.html')
