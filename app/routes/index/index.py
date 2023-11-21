from app import app
from app.blueprints import client 
from app.models import PainelUsers
from flask import url_for, redirect, render_template, request
from app.middlewares import isAuthenticated
from flask_login import current_user



@client.route("/home")
@isAuthenticated
def inicio():
    data = {
        "usersCount": PainelUsers.query.count(),
        "registeredUsers": PainelUsers.query.with_entities(PainelUsers.Id, PainelUsers.email, PainelUsers.active, PainelUsers.name, PainelUsers.date_joined, PainelUsers.type_user).all()
    }

    return render_template("dashboard/pages/home.html", user=current_user, data=data)

@app.route('/url')
def url():
    scheme = request.headers.get('X-Forwarded-Proto', request.scheme)
    host = request.headers.get('X-Forwarded-Host', request.host)
    path = request.path

    full_url = f"{scheme}://{host}{path}"
    return f"A URL real é: {full_url}"


@app.route("/")
@isAuthenticated
def route_index():
    return redirect(url_for('user.inicio'))

