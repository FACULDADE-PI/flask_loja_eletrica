from app.blueprints import admin
from app.models import PainelUsers
from app.middlewares import isAuthenticated
from flask_login import current_user
from flask import render_template




@admin.route("/edit/user")
@isAuthenticated
def route_editar_usuario():
    """ Rota de editar o usuário (apenas administrador) """
    return render_template("dashboard/pages/administrativo/editUser.html", user=current_user)
    

