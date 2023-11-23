from app.blueprints import admin
from app.models import TypeUsers
from app.middlewares import isAuthenticated
from flask_login import current_user
from flask import render_template




@admin.route("/edit/types")
@isAuthenticated
def route_editar_tipo_usuario():
    """ Rota de editar e adicionar novos tipos de usuários (apenas administrador) """
    tipos_users = TypeUsers.query.all()
    return render_template("dashboard/pages/administrativo/editTypes.html", user=current_user, types=tipos_users)
    

