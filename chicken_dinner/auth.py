import functools
from flask import (
        Blueprint,
        render_template,
        redirect,
        url_for,
        request,
        flash,
        g,
        session)


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.cursor.execute(
                "SELECT * FROM Users WHERE UserID = %s", (user_id))
        g.user = g.cursor.fetchone()


@bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        sql = "SELECT * FROM Users WHERE Name =%s ;"

        g.cursor.execute(sql, (username))
        user = g.cursor.fetchone()

        if user is None:
            flash("Incorrect Username", "name")
            error = "incorrect username"
        else:
            if password != user["Password"]:
                flash("Incorrect Password", "password")
                error = "incorrect password"

        if error:
            flash(error, 'others')
        else:
            session.clear()
            session["user_id"] = user["UserID"]
            return redirect(url_for("index.index"))

    return render_template('/auth/login.html')


@bp.route('/register')
def register():
    return render_template('/auth/register.html')


# decorator for requiring login
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
