from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    make_response
)

bp = Blueprint('market', __name__, url_prefix='/market')


@bp.route('/')
def index():
    return render_template('market/market.html')


@bp.route('/redirect')
def buy():
    url = url_for('buy.index', item_id=193)
    response = make_response(
        redirect(url, code=200)
    )
    response.headers['HX-Redirect'] = url
    return response
