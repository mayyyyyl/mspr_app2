from flask import Flask
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, UserMixin

from ldap3 import Server, Connection, ALL
server = Server('192.168.211.134')
conn = Connection(server)
print(conn.bind())

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True


# Hostname of your LDAP Server
app.config['LDAP_HOST'] = '192.168.211.134'

# Base DN of your directory
app.config['LDAP_BASE_DN'] = 'dc=MSPR,dc=local'

# Users DN to be prepended to the Base DN
app.config['LDAP_USER_DN'] = 'ou=Administrateur'

# Groups DN to be prepended to the Base DN
app.config['LDAP_GROUP_DN'] = 'ou=User'

# The RDN attribute for your user schema on LDAP
app.config['LDAP_USER_RDN_ATTR'] = 'cn'

# The Attribute you want users to authenticate to LDAP with.
app.config['LDAP_USER_LOGIN_ATTR'] = 'mail'

# The Username to bind to LDAP with
app.config['LDAP_BIND_USER_DN'] = 'Administrateur'

# The Password to bind to LDAP with
app.config['LDAP_BIND_USER_PASSWORD'] = '522-522-Ze'

login_manager = LoginManager(app)              # Setup a Flask-Login Manager
ldap_manager = LDAP3LoginManager(app)          # Setup a LDAP3 Login Manager.

# Create a dictionary to store the users in when they authenticate
# This example stores users in memory.
users = {}


# Declare an Object Model for the user, and make it comply with the
# flask-login UserMixin mixin.
class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn


# Declare a User Loader for Flask-Login.
@login_manager.user_loader
def load_user(id):
    if id in users:
        return users[id]
    return None


# Declare The User Saver for Flask-Ldap3-Login
@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    user = User(dn, username, data)
    users[dn] = user
    return user


# Import des Blueprints

from route.login import *

app.register_blueprint(login_api)



# @app.route("/manual_login")
# def manual_login():
#     # Instead of using the form, you can alternatively authenticate
#     # using the authenticate method.
#     # This WILL NOT fire the save_user() callback defined above.
#     # You are responsible for saving your users.
#     app.ldap3_login_manager.authenticate('username', 'password')

if __name__ == '__main__':
    app.run()