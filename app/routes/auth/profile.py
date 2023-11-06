from app.blueprints import client
from app.models import PainelUsers
from app.utils import verify_pass
from app.middlewares import isAuthenticated
from flask_login import current_user, UserMixin
from flask import render_template, jsonify, request




@client.route("/profile", methods=["GET"])
@isAuthenticated
def route_profile():
    """ Renderiza a view de login do usuário """
    return render_template("dashboard/pages/profile.html", user=current_user)