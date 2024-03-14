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
import random

bp = Blueprint('market', __name__, url_prefix='/market')

itemArray = []

modifiedArray = []

search_term = ''

sortMethod = 'Default'

minPrice = ''

maxPrice = ''


def load_items():
    global itemArray
    print("fetching")
    sql = "SELECT ItemID, NFT_Item.Name, NFT_Item.UserID, Users.Name, Price FROM NFT_Item INNER JOIN Users ON NFT_Item.UserID = Users.UserID WHERE NFT_Item.UserID != %s"
    g.cursor.execute(sql, (g.user["UserID"]))
    itemArray = g.cursor.fetchall()
    return itemArray


@bp.route('/search', methods=["POST"])
def search():
    global modifiedArray, search_term, minPrice, maxPrice, sortMethod

    search_term = request.form['search']
    
    modifiedArray = search_func(itemArray, search_term)

    if (minPrice != '' and maxPrice != ''):
        modifiedArray = filter_func(modifiedArray, minPrice, maxPrice)

    if (sortMethod != 'Default'):
        modifiedArray = sort_func(modifiedArray, sortMethod)
    
    html = print_item(modifiedArray)
    return html


def search_func(itemArray, search_term):
    resultArray = []
    if search_term == '':
        resultArray = itemArray
    else:
        for item in itemArray:
            if item["Name"].lower().startswith(search_term.lower()):
                resultArray.append(item)
    
    return resultArray


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
        html += 'View'
        html += '</button>'
        html += f'<button hx-get="./trades/{item["ItemID"]}" style="margin-left: 1.5%;">'
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
    
    randomSample = random.sample(itemArray, 5)

    return render_template('market/market.html', itemArray=itemArray, featuredArray=randomSample)


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


@bp.route('/sort')
def sort():
    global modifiedArray, sortMethod
    sortMethod = request.args.get('sort')
    
    modifiedArray = sort_func(modifiedArray, sortMethod)

    html = print_item(modifiedArray)
    return html


def sort_func(itemArray, sortMethod):
    resultArray = []

    if (sortMethod == "Price:HtL"):
        resultArray = sorted(itemArray, key = lambda d : d["Price"], reverse = True)
    elif (sortMethod == "Price:LtH"):
        resultArray = sorted(itemArray, key = lambda d : d["Price"], reverse = False)
    else:
        resultArray = sorted(itemArray, key = lambda d : d["ItemID"], reverse = False)

    return resultArray


@bp.route('/filter', methods = ["POST"])
def filter():
    global modifiedArray, search_term, minPrice, maxPrice, sortMethod

    minPrice = request.form['min']
    maxPrice = request.form['max']

    modifiedArray = filter_func(itemArray, minPrice, maxPrice)

    if (search_term != ''):
        modifiedArray = search_func(modifiedArray, search_term)

    if (sortMethod != 'Default'):
        modifiedArray = sort_func(modifiedArray, sortMethod)
       
    html = print_item(modifiedArray)
    return html


def filter_func(itemArray, minPrice, maxPrice):
    resultArray = []
    if (maxPrice == '' or minPrice ==  ''):
        resultArray = itemArray
    else:
        for item in itemArray:
            if ((item["Price"] >= float(minPrice)) and (item["Price"] <= float(maxPrice))):
                resultArray.append(item)
    
    return resultArray




