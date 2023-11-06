from app.blueprints import auth
from app.models import PainelUsers
from app import db
from flask import render_template, jsonify, request


@auth.route("/register", methods=["GET"])
def route_register():
    """ Renderiza a view de efetuar o registro do usuário """
    return render_template("auth/register.html")



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
    if Users.query.filter_by(email=email_usuario.lower()).first():
        return jsonify({
            "icon": "error",
            "title": "Oops, algo deu errado.",
            "text": "Já existe um usuário registrado com este email."
        }), 200


    new_user = Users(
        email=email_usuario.lower(),
        password=senha_usuario1,
        name=nome_usuario
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "icon": "success",
        "title": "Sucesso!",
        "text": "Usuário cadastrado com sucesso."
    }), 200
