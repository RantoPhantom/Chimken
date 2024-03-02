from .auth import login_required
from .db import Database
from flask import (
        Blueprint,
        render_template,
        url_for,
        redirect,
        request,
        make_response
        )

bp = Blueprint('market', __name__, url_prefix='/market')

item1 = {
        'id': '01',
        'img': 'img2.jpg',
        'name': 'Pipipopo',
        'price': '9.75'
        }

item2 = {
        'id': '02',
        'img': 'img6.jpg',
        'name': 'Bopeep',
        'price': '10.0'
        }

item3 = {
        'id': '03',
        'img': 'img5.jpg',
        'name': 'Beepo',
        'price': '13.0'
        }

itemArray = [item1, item2, item3, item1, item2]


@bp.route('/search', methods=["POST"])
def search():
    search_term = request.form['search']

    return search_term


@bp.route('/')
@login_required
def index():

    return render_template('market/market.html', itemArray=itemArray)


@bp.route('/redirect/<int:item_id>')
@login_required
def lol(item_id):
    url = url_for('buy.index', item_id=item_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response
