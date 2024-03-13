import functools
from flask import (Blueprint, render_template, request, url_for, g, make_response, redirect)
from .auth import login_required

bp = Blueprint('index', __name__, url_prefix='/')


def load_items():
    sql = "SELECT ItemID, NFT_Item.Name, NFT_Item.UserID, Users.Name, Price FROM NFT_Item INNER JOIN Users ON NFT_Item.UserID = Users.UserID WHERE NFT_Item.UserID != %s ORDER BY RAND() LIMIT 5"
    g.cursor.execute(sql, (g.user["UserID"]))
    itemArray = g.cursor.fetchall()
    return itemArray

def load_users():
    sql = "SELECT UserID, Name, (SELECT COUNT(*) FROM NFT_Item WHERE NFT_Item.UserID = Users.UserID) AS OwnedNFT FROM Users WHERE UserID != %s ORDER BY RAND() LIMIT 5"
    g.cursor.execute(sql, (g.user["UserID"]))
    userArray = g.cursor.fetchall()

    return userArray


@bp.route('/')
@login_required
def index():
    itemArray = load_items()
    userArray = load_users()

    return render_template('index/index.html', g=g, itemArray = itemArray, userArray = userArray)

@bp.route('/markett/', methods=["GET"])
def markett():
    return redirect(url_for('market.index'))


@bp.route('/profile/<int:user_id>/', methods=["GET"])
def profile(user_id):
    url = url_for('profile.index', user_id = user_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response


@bp.route('/trades/<int:item_id>/', methods=["GET"])
def trade(item_id):
    url = url_for('trades.index', item_id=item_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response


@bp.route('/redirect/<int:item_id>/')
def lol(item_id):
    url = url_for('buy.index', item_id=item_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response