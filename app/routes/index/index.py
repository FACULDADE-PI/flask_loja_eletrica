from app import app
from flask import url_for


@app.route("/")
def route_index():
    return url_for('auth.route_login')