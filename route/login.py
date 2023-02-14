from flask import Blueprint, redirect, url_for, render_template_string, render_template
from flask_ldap3_login.forms import LDAPLoginForm
from flask_login import login_user, current_user

login_api = Blueprint('login_api', __name__)


@login_api.route("/")
def home():
    # Redirect users who are not logged in.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('login_api.login'))

    return render_template("home.html")


@login_api.route('/login', methods=['GET', 'POST'])
def login():
    template = """
    {{ get_flashed_messages() }}
    {{ form.errors }}
    <form method="POST">
        <label>Username{{ form.username() }}</label>
        <label>Password{{ form.password() }}</label>
        {{ form.submit() }}
        {{ form.hidden_tag() }}
    </form>
    """

    # Instantiate a LDAPLoginForm which has a validator to check if the user
    # exists in LDAP.
    form = LDAPLoginForm()

    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object
        # via form.user.
        login_user(form.user)  # Tell flask-login to log them in.
        return redirect('/')  # Send them home

    return render_template_string(template, form=form)