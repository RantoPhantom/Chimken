from __init__ import app
from flask import render_template


@app.route('/')
def test():
    return render_template('index.html')
