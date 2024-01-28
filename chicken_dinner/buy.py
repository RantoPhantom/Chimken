from flask import (Blueprint, render_template, Response)
import matplotlib.pyplot as plt
from io import BytesIO
bp = Blueprint('buy', __name__, url_prefix='/buy')


@bp.route('/<int:item_id>')
def buy(item_id):
    # temp
    item = {
        'name': 'LMAO',
        'price': 69.420,
        'currency': 'VND',
        'author': 'lol'
    }

    return render_template('buy/buy.html', item=item)


@bp.route('/lol')
def lol():
    return "hey"


@bp.route('/pricing_history')
def pricing_history():
    # Retrieve pricing data (replace with your actual data retrieval logic)
    # For example, you might fetch data from a database
    dates = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
    prices = [100, 110, 105, 115, 120]

    # Create the chart
    plt.plot(dates, prices)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Pricing History')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Convert the plot to a binary image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Clear the plot to avoid memory leaks
    plt.clf()

    # Return the binary image as a Flask response
    return Response(buffer.getvalue(), mimetype='image/png')
