import functools
import random
from flask import (Blueprint, render_template, request, url_for, g)
from .auth import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')

itemArray = []


def load_dtb():
    g.cursor.execute('SELECT * from NFT_Item')
    result = g.cursor.fetchall()
    for x in result:
        item = {
                'id': x[0],
                'name': x[1],
                'price': x[3],
                'desc': x[4]
        }
        itemArray.append(item)

    return 0


user1 = {
        "id": "3",
        "name": "Chicken Dinner Winner"
}

userArray = [user1]

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


@bp.route('/')
@login_required
def index():
    if (len(itemArray) == 0):
        load_dtb()
    return render_template('profile/profile.html', itemArray=itemArray, userArray=userArray, statusArray=statusArray, 
                           ethArray=ethArray)
