from flask import (Blueprint, render_template, g, url_for, make_response, redirect)

bp = Blueprint('buy', __name__, url_prefix='/buy')


@bp.route('/<int:item_id>')
def index(item_id):
    sql = "SELECT ItemID, NFT_Item.Name, NFT_Item.UserID, Users.Name, Price, Description FROM NFT_Item INNER JOIN Users ON NFT_Item.UserID = Users.UserID WHERE ItemID = %s"
    g.cursor.execute(sql, (item_id))
    item = g.cursor.fetchone()

    return render_template('buy/buy.html', item=item)


# @bp.route('/get-listing-data', methods=['POST'])
# def get_listing_data():
#     html_response = ""

#     listing_data = []

#     lol = {
#         'unit_price': '69.420 ETH',
#         'quantity': 1,
#         'expiration': '29 years',
#         'from': 'Username'
#     }

#     listing_data.append(lol)
#     listing_data.append(lol)
#     listing_data.append(lol)

#     html_response = ""
#     for listing in listing_data:
#         html_response += "<tr>"
#         for key, value in listing.items():
#             html_response += f"<td>{value}</td>"
#         html_response += "</tr>"
#     return html_response

@bp.route('/profile/<int:user_id>', methods=["GET"])
def profile(user_id):
    url = url_for('profile.index', user_id = user_id)
    response = make_response(
            redirect(url, code=200)
            )
    response.headers['HX-Redirect'] = url
    return response
