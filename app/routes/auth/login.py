from app.blueprints import auth
from app.models import PainelUsers
from app.utils import verify_pass
from app.middlewares import ifAuthenticatedGoIndex
from flask_login import current_user, UserMixin, login_user, logout_user
from flask import render_template, jsonify, request, redirect




@auth.route("/login", methods=["GET"])
@ifAuthenticatedGoIndex
def route_login():
    """ Renderiza a view de login do usuário """
    return render_template("auth/login.html")





@auth.route("/logout/user", methods=["POST", "GET"])
def route_logout():
    """ Efetua o logout do usuário """
    user:UserMixin = current_user
    if not user.is_authenticated and request.method == "POST":
        return jsonify({
            "icon": "error",
            "title": "Oops!",
            "text": "Você não está logado"
        }), 200

    if user.is_authenticated:
        logout_user()

    if request.method == "POST":
        return jsonify({
            "icon": "success",
            "title": "Usuário saiu.",
            "text": "Você saiu do painel com sucesso."
        }), 200
    
    else:
        return redirect("/")


@auth.route("/login/user", methods=["POST"])
def route_login_user():
    """ Efetua o login do usuário """
    
    user:UserMixin = current_user
    if user.is_authenticated:
        return jsonify({
            "icon": "success",
            "title": "Usuário autenticado.",
            "text": "Você já estava logado préviamente."
        }), 200


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

    user = PainelUsers.query.filter_by(email=email_usuario.lower()).first()
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
    

    login_user(user, remember=True)
    return jsonify({
        "icon": "success",
        "title": "Usuário autenticado.",
        "text": "Você foi autenticado com sucesso."
    }), 200



    