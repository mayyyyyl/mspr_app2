# Installer le projet

git clone
py -m venv venv
.\venv\scripts\activate
pip install -r requirements.txt

$env:FLASK_APP = "app"
flask run