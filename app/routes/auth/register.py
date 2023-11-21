from app.blueprints import auth
from app.models import PainelUsers
from app.middlewares import paramsRequired
from app.utils import send_mail_activation
from app import db, tokenSafe, app
from flask import render_template, jsonify, request, abort, redirect
from flask_login import login_user
from app.middlewares import ifAuthenticatedGoIndex
from itsdangerous import SignatureExpired


@auth.route("/register", methods=["GET"])
@ifAuthenticatedGoIndex
def route_register():
    """ Renderiza a view de efetuar o registro do usuário """
    return render_template("auth/register.html")




@auth.route("/register/confirm", methods=["POST", "GET"])
@paramsRequired(["token"])
def route_confirm_registration():
    """ Confirma o registro do usuário recebendo o GET ou POST do link enviado para o email """
    try:
        email_token = tokenSafe.loads(
            request.args['token'], 
            salt=app.config.get("TOKEN_SALT"), 
        )

        user:PainelUsers = PainelUsers.query.filter_by(email=email_token).first()
        user.active = True
        db.session.commit()
        login_user(user)    

    except (Exception) as err:
        print(err)
        return abort(404)

    return redirect("/")




@auth.route("/register/new", methods=["POST"])
def route_register_new_user():
    """ Efetua o registro do usuário """
    email_usuario = request.form.get("email_usuario", "")
    nome_usuario = request.form.get("nome_usuario", "")
    senha_usuario1 = request.form.get("senha_usuario_1", "")
    senha_usuario2 = request.form.get("senha_usuario_2", "")

    if senha_usuario1 != senha_usuario2:
        return jsonify({
            "icon": "error",
            "title": "Senhas não coincidem.",
            "text": "Revise os dados e tente novamente."
        }), 200

    if "@" not in email_usuario or len(email_usuario) < 6:
        return jsonify({
            "icon": "error",
            "title": "Oops, algo deu errado.",
            "text": "O seu email é inválido."
        }), 200
    
    if len(senha_usuario1) < 6 or len(senha_usuario2) < 6:
        return jsonify({
            "icon": "error",
            "title": "Oops, algo deu errado.",
            "text": "A sua senha deve possuir no mínimo 6 caracteres"
        }), 200
    
    if len(nome_usuario) < 4:
        return jsonify({
            "icon": "error",
            "title": "Oops, algo deu errado.",
            "text": "O seu nome é inválido."
        }), 200
    
    # VALIDA NO BANCO
    if PainelUsers.query.filter_by(email=email_usuario.lower()).first():
        return jsonify({
            "icon": "error",
            "title": "Oops, algo deu errado.",
            "text": "Já existe um usuário registrado com este email."
        }), 200


    new_user = PainelUsers(
        email=email_usuario.lower(),
        password=senha_usuario1,
        name=nome_usuario,
        active=False
    )
    
    db.session.add(new_user)
    db.session.commit()

    send_mail_activation(email_usuario.lower(), nome_usuario)

    return jsonify({
        "icon": "success",
        "title": "Sucesso!",
        "text": "Usuário cadastrado. Complete a ativação do perfil clicando no link enviado para o email."
    }), 200
