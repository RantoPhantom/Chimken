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

<<<<<<< Updated upstream
    return 0
=======

def load_items():
    global itemArray
    print("fetching")
    g.cursor.execute("SELECT ItemID, NFT_Item.Name, Users.Name, Price FROM NFT_Item INNER JOIN Users ON NFT_Item.UserID = Users.UserID")
    itemArray = g.cursor.fetchall()
    print(itemArray)
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

@bp.route('/sort-htl')
def sort_htl():
    html_respond = f"<span> Price: High to Low </span>" 
    return html_respond 

@bp.route('/sort-lth')
def sort_lth():
    html_respond = f"<span> Price: Low to High </span>" 
    return html_respond 

@bp.route('/sort-default')
def no_sort():
    html_respond = f"<span> Price: Default </span>" 
    return html_respond 

def print_item(itemList):
    html = ''
    for item in itemList:
        html += '<div class="featured-items market-NFT">'
        html += '<div class="featured-img">'
        html += f'<img src="../static/img/img{item["ItemID"]}.jpg"/>'
        html += '</div>'

        html += '<div class="featured-info">'
        html += f'<h2>{item["Name"]}</h2>'
        html += f'<a href=""> {item["Users.Name"]} </a>'

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
>>>>>>> Stashed changes


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

<<<<<<< Updated upstream
@bp.route('/lol/<int:item_id>')
def lol(item_id):
    url = url_for('buy.index', item_id=item_id)
    response = make_response(
        redirect(url, code=200)
    )
    response.headers['HX-Redirect'] = url
    return response
=======

@bp.route('/trade/<int:item_id>', methods=["GET"])
def trade(item_id):
    url = url_for('trades.index', item_id=item_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response
    
    
>>>>>>> Stashed changes
