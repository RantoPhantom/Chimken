from flask import (Blueprint, render_template)
import plotly.graph_objs as go

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
    # Sample data
    x_data = [1, 2, 3, 4, 5]
    y_data = [10, 15, 13, 17, 18]

    # Pass data to HTML template
    return render_template('buy/buy.html', x_data=x_data, y_data=y_data, item=item)

# def buy(item_id):
#    # temp
#    item['id'] = item_id
#
#    # Sample data
#    x_data = [1, 2, 3, 4, 5]
#    y_data = [10, 15, 13, 17, 18]
#
#    # Create Plotly figure
#    fig = go.Figure()
#    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='line'))
#
#    fig.update_layout(
#        title='Pricing History',
#        xaxis_title='Time',
#        yaxis_title='Price',
#        plot_bgcolor='rgba(0,0,0,0)',
#        paper_bgcolor='rgba(0,0,0,0)',
#        font=dict(color='white'),  # Set font color
#        margin=dict(l=1, r=1, t=100, b=1),
#        yaxis_showgrid=False,  # Make x-axis gridlines invisible
#        showlegend=False,
#
#    )
#
#    plot_json = fig.to_json()
#    return render_template('buy/buy.html', item=item, plot_json=plot_json)
