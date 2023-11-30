from app import app
from app.blueprints import client 
from app.models import PainelUsers
from flask import url_for, redirect, render_template, request
from app.middlewares import isAuthenticated
from flask_login import current_user



@client.route("/home")
@isAuthenticated
def inicio():
    """ Index """
    data = {
        "usersCount": PainelUsers.query.count(),
        "registeredUsers": PainelUsers.query.with_entities(PainelUsers.Id, PainelUsers.email, PainelUsers.active, PainelUsers.name, PainelUsers.date_joined, PainelUsers.type_user).all()
    }

    return render_template("dashboard/pages/user/home.html", user=current_user, data=data)


@app.route("/")
@isAuthenticated
def route_index():
    return redirect(url_for('user.inicio'))

