from .auth import login_required
from flask import (
        Blueprint,
        render_template,
        url_for,
        redirect,
        request,
        g,
        make_response
        )

bp = Blueprint('market', __name__, url_prefix='/market')

itemArray = []

sortMethod = ''

def load_items():
    global itemArray
    print("fetching")
    sql = "SELECT ItemID, NFT_Item.Name, NFT_Item.UserID, Users.Name, Price FROM NFT_Item INNER JOIN Users ON NFT_Item.UserID = Users.UserID WHERE NFT_Item.UserID != %s"
    g.cursor.execute(sql, (g.user["UserID"]))
    itemArray = g.cursor.fetchall()
    return itemArray


@bp.route('/search', methods=["POST"])
def search():
    search_term = request.form['search']
    item_to_print = []
    if search_term == '':
        item_to_print = itemArray
    else:
        for item in itemArray:
            if item["Name"].lower().startswith(search_term.lower()):
                item_to_print.append(item)
    html = print_item(item_to_print)
    return html


def print_item(itemList):
    html = ''
    for item in itemList:
        html += '<div class="featured-items market-NFT">'
        html += '<div class="featured-img">'
        html += f'<img src="../static/img/nft/img{item["ItemID"]}.jpg"/>'
        html += '</div>'

        html += '<div class="featured-info">'
        html += f'<h2>{item["Name"]}</h2>'
        html += f'<a href="" hx-get="./profile/{item["UserID"]}"> @{item["Users.Name"]} </a>'

        html += '<div class="featured-price">'
        html += '<p style="font-size: 92%;">Price:</p>'
        html += f'<p style="font-size: 84.6%">{item["Price"]}ETH</p>'
        html += '</div>'

        html += '<div class="featured-button">'
        html += f'<button hx-get="./redirect/{item["ItemID"]}" style="margin-right: 1.5%;">'
        html += 'Buy'
        html += '</button>'
        html += '<button style="margin-left: 1.5%;">'
        html += 'Trade'
        html += '</button>'
        html += '</div>'
        html += '</div>'
        html += '</div>'
        html += '</div>'
    return html


@bp.route('/')
@login_required
def index():
    global itemArray
    itemArray = load_items()
    return render_template('market/market.html', itemArray=itemArray)


@bp.route('/redirect/<int:item_id>')
def lol(item_id):
    url = url_for('buy.index', item_id=item_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response


@bp.route('/trades/<int:item_id>', methods=["GET"])
def trade(item_id):
    url = url_for('trades.index', item_id=item_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response


@bp.route('/profile/<int:user_id>', methods=["GET"])
def profile(user_id):
    url = url_for('profile.index', user_id = user_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response



