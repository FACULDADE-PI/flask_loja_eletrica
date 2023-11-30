from app import db
from app.blueprints import admin
from app.models import TypeUsers
from app.middlewares import isAuthenticated, paramsRequired, hasPrivileges
from flask_login import current_user
from flask import render_template, jsonify, request



@admin.route("/edit/types")
@isAuthenticated
@hasPrivileges(["Administrador", "Programador"])
def route_editar_tipo_usuario():
    """ Rota de editar e adicionar novos tipos de usuários (apenas administrador) """
    tipos_users = TypeUsers.query.all()
    return render_template(
        "dashboard/pages/administrativo/editTypes.html", user=current_user, types=tipos_users)



@admin.route("/edit/types/confirm", methods=["POST"])
@isAuthenticated
@paramsRequired(["idType", "descriptionType", "slugType", "isActive"])
@hasPrivileges(["Administrador", "Programador"])
def confirmar_edicao_tipo_usuario():
    """ Rota de editar o tipo de usuário """
    type_id = int(request.form["idType"])
    if type_id in (1, 2, 3):
        return jsonify({
            "icon": "error",
            "title": "Oops!",
            "text": "Não é possível realizar alterações nesse tipo de usuário."
        }), 200


    typeUser:TypeUsers = TypeUsers.query.get(type_id)
    if not typeUser:
        return jsonify({
            "icon": "error",
            "title": "Oops!",
            "text": "O tipo de usuário não pôde ser encontrado. A alteração não foi realizada."
        }), 200

    typeUser.slug = request.form["slugType"]
    typeUser.description = request.form["descriptionType"]
    typeUser.active = bool(int(request.form["isActive"]))

    db.session.commit()

    return jsonify({
        "icon": "success",
        "title": "Sucesso!",
        "text": "A alteração do tipo de usuário foi realizada com sucesso!"
    }), 200



@admin.route("/edit/types/status/change", methods=["POST"])
@isAuthenticated
@paramsRequired(["idType"])
@hasPrivileges(["Administrador", "Programador"])
def alterar_status_tipo_usuario():
    """ Rota de mudar o status do tipo de usuário """
    type_id = int(request.form["idType"])
    typeUser:TypeUsers = TypeUsers.query.get(type_id)

    if not typeUser:
        return jsonify({
            "icon": "error",
            "title": "Oops!",
            "text": "O tipo de usuário não pôde ser encontrado. A alteração não foi realizada."
        }), 200

    typeUser.active = int(not typeUser.active)
    db.session.commit()

    return jsonify({
        "icon": "success",
        "title": "Sucesso!",
        "text": "O tipo de usuário foi reativado com sucesso" if typeUser.active else "O tipo de usuário foi desativado com sucesso"
    }), 200


@admin.route("/edit/types/new", methods=["POST"])
@isAuthenticated
@paramsRequired(["descriptionType", "slugType", "isActive"])
@hasPrivileges(["Administrador", "Programador"])
def novo_tipo_usuario():
    """ Adiciona um novo tipo de usuário no sistema """
    
    new_type:TypeUsers = TypeUsers(
        description=request.form["descriptionType"],
        slug=request.form["slugType"],
        active=bool(int(request.form["isActive"]))
    )

    db.session.add(new_type)
    db.session.commit()

    return jsonify({
        "icon": "success",
        "title": "Sucesso!",
        "text": "O novo tipo de usuário foi adicionado com sucesso"
    }), 200
