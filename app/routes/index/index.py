from app import app
from app.blueprints import client 
from flask import url_for, redirect, render_template
from app.middlewares import isAuthenticated
from flask_login import current_user



@client.route("/inicio")
@isAuthenticated
def inicio():
    return render_template("dashboard/pages/inicio.html", user=current_user)


@app.route("/")
@isAuthenticated
def route_index():
    return redirect(url_for('user.inicio'))