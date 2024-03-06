import os
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

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

    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'lol'
    app.config['MYSQL_DATABASE_DB'] = 'chimken_dinner'
    app.config['MYSQL_DATABASE_HOST'] = 'sql-lol.duckdns.org'
    db = MySQL()
    db.init_app(app)

    # Register a function to run before each request
    @app.before_request
    def before_request():
        conn = db.connect()
        cursor = conn.cursor(DictCursor)
        # Store the database connection in the application context's 'g' object
        g.conn = conn
        g.cursor = cursor

    from . import auth
    app.register_blueprint(auth.bp)

    from . import trades
    app.register_blueprint(trades.bp)

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
