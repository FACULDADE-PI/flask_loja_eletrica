from app.blueprints import auth
from app.models import Users
from app.utils import verify_pass
from flask import render_template, jsonify, request


@auth.route("/login", methods=["GET"])
def route_login():
    """ Renderiza a view de login do usuário """
    return render_template("auth/login.html")


@auth.route("/login/user", methods=["POST"])
def route_login_user():
    """ Efetua o login do usuário """
    
    email_usuario = request.form.get("email_usuario", "")
    senha_usuario = request.form.get("senha_usuario", "")

    if "@" not in email_usuario or len(email_usuario) < 6:
        return jsonify({
            "icon": "error",
            "title": "Oops, algo deu errado.",
            "text": "O seu email é inválido."
        }), 200
    
    if len(senha_usuario) < 6:
        return jsonify({
            "icon": "error",
            "title": "Oops, algo deu errado.",
            "text": "A sua senha deve possuir no mínimo 6 caracteres"
        }), 200

    user = Users.query.filter_by(email=email_usuario.lower()).first()
    if not user:
        return jsonify({
            "icon": "error",
            "title": "Usuário inexistente.",
            "text": "O usuário não está registrado. Você pode registrar um novo usuário a qualquer momento."
        }), 200

    if not verify_pass(senha_usuario, user.password):
        return jsonify({
            "icon": "error",
            "title": "Senha incorreta.",
            "text": "A senha inserida está incorreta. Corrija os dados e refaça o login."
        }), 200
    
    return jsonify({
        "icon": "success",
        "title": "Usuário autenticado.",
        "text": "Você foi autenticado com sucesso."
    }), 200



    