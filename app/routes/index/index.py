from app import app
from flask import url_for, redirect


@app.route("/")
def route_index():
    return redirect(url_for('auth.route_login'))