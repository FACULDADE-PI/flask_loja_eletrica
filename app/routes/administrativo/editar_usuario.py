from app import db
from app.blueprints import admin
from app.models import PainelUsers, TypeUsers
from app.middlewares import isAuthenticated, hasPrivileges, paramsRequired
from flask_login import current_user
from flask import render_template, request, jsonify


@admin.route("/edit/user")
@isAuthenticated
@hasPrivileges(["Administrador", "Programador"])
def route_editar_usuario():
    """ Rota de editar o usuário (apenas administrador) """

    users_with_type_details = (
        db.session.query(
            PainelUsers.Id,
            PainelUsers.email,
            PainelUsers.active,
            PainelUsers.name,
            PainelUsers.date_joined,
            PainelUsers.type_user,
            TypeUsers.slug.label('type_user_slug'),
        )
        .join(TypeUsers, PainelUsers.type_user == TypeUsers.Id)
        .all()
    )

    quantidadeUsuarios = PainelUsers.query.filter(PainelUsers.active == 1).count()
    tipoUsuarios = TypeUsers.query.all()

    data = {
        "usersCount": quantidadeUsuarios,
        "registeredUsers": users_with_type_details,
        "typeUsers": tipoUsuarios
    }
    
    return render_template("dashboard/pages/administrativo/editUser.html", user=current_user, data=data)



@admin.route("/edit/user/confirm", methods=["POST"])
@isAuthenticated
@paramsRequired(["idUser", "nameUser", "slugUser"])
@hasPrivileges(["Administrador", "Programador"])
def confirmar_edicao_usuario():
    """ Rota de editar o usuário (apenas administrador) """

    findedUser = PainelUsers.query.filter_by(Id=request.form["idUser"]).first()
    if not findedUser:
        return jsonify({
            "icon": "error",
            "title": "Oops!",
            "text": "O usuário não foi encontrado." 
        }), 200
    
    if findedUser.type_user == 1:
        return jsonify({
            "icon": "error",
            "title": "Oops!",
            "text": "Impossível editar esse tipo de usuário." 
        }), 200

    findedUser.name = request.form["nameUser"]
    findedUser.type_user = int(request.form["slugUser"])

    db.session.commit()

    return jsonify({
        "icon": "success",
        "title": "Sucesso!",
        "text": "O usuário foi editado com sucesso." 
    }), 200



@admin.route("/edit/user/status", methods=["POST"])
@isAuthenticated
@paramsRequired(["idUser"])
@hasPrivileges(["Administrador", "Programador"])
def editar_status_usuario():
    """ Desabilita ou habilita o usuário """

    findedUser:PainelUsers = PainelUsers.query.filter_by(Id=int(request.form["idUser"])).first()
    if not findedUser:
        return jsonify({
            "icon": "error",
            "title": "Oops!",
            "text": "O usuário não foi encontrado." 
        }), 200
    

    findedUser.active = not findedUser.active
    db.session.commit()

    return jsonify({
        "icon": "success",
        "title": "Sucesso!",
        "text": "O status do usuário foi alterado para {} com sucesso".format("ativo" if findedUser.active else "inativo")
    }), 200
