import functools
import random
from flask import (Blueprint, render_template, request, url_for, g)
from .auth import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')

itemArray = []

userArray = []


def load_items(user_id):
    global itemArray
    print("fetching")
    g.cursor.execute("SELECT * FROM NFT_Item WHERE UserID = %s", (user_id,))
    itemArray = g.cursor.fetchall()     
    return itemArray

def load_users(user_id):
    global userArray
    g.cursor.execute("SELECT * FROM Users WHERE UserID = %s", (user_id,))
    userArray = g.cursor.fetchall()     
    return userArray

status1 = {
        "color": "#6EC531",
        "name": "Active",
}

status2 = {
        "color": "#D3D3D3",
        "name": "Inactive",
}

status3 = {
        "color": "#CC0202",
        "name": "Cancel",
}

statusArray = [status1, status2, status3]

eth1 = {
        "plus": "+ 2.3ETH"
}

eth2 = {
        "plus": "+ 6.9ETH"
}

eth3 = {
        "plus": "+ 8.12ETH"
}

ethArray = [eth1, eth2, eth3]

trade_info = {
    "hash": "0xdC0b8cA898DB8D46A37517d70E63985ABA1FaF0B",
    "block": "hong biet cai nay =))",
}

trade_infoArray = [trade_info]


@bp.route('/<int:user_id>', methods=["GET"])
@login_required
def index(user_id):
    print(user_id)
    is_own_profile = False
    if user_id == g.user["UserID"]:
        is_own_profile = True
    load_items(user_id) 
    load_users(user_id)   
    return render_template('profile/profile.html', itemArray=itemArray, userArray=userArray, statusArray=statusArray, 
                           ethArray=ethArray, trade_infoArray=trade_infoArray, is_own_profile=is_own_profile)
