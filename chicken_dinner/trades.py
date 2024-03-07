import functools
from flask import (Blueprint, render_template, redirect, flash, request, url_for, g)

bp = Blueprint('trades', __name__, url_prefix='/trades')

@bp.route('/<int:item_id>', methods=["GET"])
def index(item_id):
    sql = "SELECT ItemID, NFT_Item.Name, Users.Name, Price FROM NFT_Item INNER JOIN Users ON NFT_Item.UserID = Users.UserID WHERE ItemID = %s"
    g.cursor.execute(sql, (item_id))
    item = g.cursor.fetchone()
    
    sql = "SELECT * FROM NFT_Item WHERE UserID = %s"
    g.cursor.execute(sql, (g.user["UserID"]))
    itemArray = g.cursor.fetchall()

    return render_template('trades/trades.html', item = item, itemArray = itemArray)

@bp.route('/<int:item_id>', methods=('GET', 'POST'))
def get_data(item_id):
    if request.method == 'POST':
        tradeList = request.form.getlist('trades-item')
        if len(tradeList) > 2:
            flash("More than two NFTs selected", "limit")
            return redirect(url_for('trades.index', item_id = item_id))
        elif len(tradeList) == 0:
            flash("No NFT selected", "limit")
            return redirect(url_for('trades.index', item_id = item_id))
        else:
            addEth = request.form['add-eth']
            reqEth = request.form['req-eth']
        
        print(item_id)
        print(addEth)
        print(reqEth)
        print(request.form.getlist('trades-item'))


    return redirect(url_for('market.index'))