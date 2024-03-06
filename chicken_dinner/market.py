from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    make_response,
    g
)

bp = Blueprint('market', __name__, url_prefix='/market')

itemArray = []

def load_dtb():
    g.cursor.execute('SELECT * from NFT_Item')
    result = g.cursor.fetchall()
    
    for x in result:
        item = {
            'id' : x[0],
            'name' : x[1],
            'price' : x[3]
        }
        itemArray.append(item)

    return 0


@bp.route('/')
def index():
    if (len(itemArray) == 0):
        load_dtb()

    return render_template('market/market.html', itemArray = itemArray)

@bp.route('/sort')
def sort():
    html_respond = "<span> Changed </span>" 
    return html_respond 

@bp.route('/redirect')
def buy():
    url = url_for('buy.index', item_id=193)
    response = make_response(
        redirect(url, code=200)
    )
    response.headers['HX-Redirect'] = url
    return response

@bp.route('/lol/<int:item_id>')
def lol(item_id):
    url = url_for('buy.index', item_id=item_id)
    response = make_response(
        redirect(url, code=200)
    )
    response.headers['HX-Redirect'] = url
    return response