import os
from .db import Database
from flask import Flask, g


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # INIT BLUEPRINTS AND DB HERE

    db = Database()
    db.init_app(app)

    @app.before_request
    def before_request():
        # ping to keep db alive
        db.get_db().ping()

        g.conn = db.get_db()
        g.cursor = db.get_cursor()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import buy
    app.register_blueprint(buy.bp)

    from . import market
    app.register_blueprint(market.bp)

    from . import index
    app.register_blueprint(index.bp)

    from . import profile
    app.register_blueprint(profile.bp)

    from . import create
    app.register_blueprint(create.bp)

    return app
