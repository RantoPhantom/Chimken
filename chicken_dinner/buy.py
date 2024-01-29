from flask import (Blueprint, render_template)
import plotly.graph_objs as go

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
    return "<p>hey</p>"


@bp.route('/chart')
def index():
    item = {
        'name': 'LMAO',
        'price': 69.420,
        'currency': 'VND',
        'author': 'lol'
    }
    # Sample data
    x_data = [1, 2, 3, 4, 5]
    y_data = [10, 15, 13, 17, 18]

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='line'))

    # Convert Plotly figure to JSON
    plot_json = fig.to_json()

    return render_template('buy/buy.html', plot_json=plot_json, item=item)
