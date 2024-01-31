from flask import (Blueprint, render_template)

bp = Blueprint('buy', __name__, url_prefix='/buy')

item = {
    'id': 0,
    'name': 'PipPog',
    'price': '69.420',
    'currency': 'Balls',
    'author': 'Pippa'
}


@bp.route('/<int:item_id>')
def index(item_id):
    item['id'] = item_id
    # Pass data to HTML template
    return render_template('buy/buy.html', item=item)


@bp.route('/get-listing-data', methods=['POST'])
def get_listing_data():
    html_response = ""

    listing_data = []

    lol = {
        'unit_price': 100,
        'quantity': 12,
        'expiration': '29 years',
        'from': 'me'
    }

    listing_data.append(lol)

    html_response = ""
    for listing in listing_data:
        html_response += "<tr>"
        for key, value in listing.items():
            html_response += f"<td>{value}</td>"
        html_response += "</tr>"
        return html_response
