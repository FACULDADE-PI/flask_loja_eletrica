from app import app, tokenSafe, db
from app.blueprints import auth
from app.models import PainelUsers
from app.utils import hash_pass, send_mail_reset
from app.middlewares import paramsRequired
from flask_login import current_user, logout_user, UserMixin
from flask import render_template, jsonify, request, redirect, abort, url_for
from itsdangerous import SignatureExpired




@auth.route("/reset/password", methods=["GET"])
def route_redefinir():
    """ Renderiza a view de redefinir a senha do usuário """
    user:UserMixin = current_user
    if user.is_authenticated:
        return redirect("/")
    
    return render_template("auth/redefine.html")


@auth.route("/reset/password/fill", methods=["POST", "GET"])
@paramsRequired(["token"])
def reset_password_using_token():
    """ Redefine a senha utilizando o token enviado para o email """

    try:
        tokenSafe.loads(
            request.args['token'], 
            salt=app.config.get("TOKEN_SALT"), 
            max_age=int(app.config.get('EXPIRATION_TOKEN', ''))*60
        )

    except (SignatureExpired):
        return redirect(url_for('auth.route_redefinir'))

    except (Exception) as err:
        print(err)
        return abort(404)

    if current_user.is_authenticated:
        logout_user(current_user)

    return render_template("/auth/new_password.html")



@auth.route("/reset/password/completion", methods=["POST"])
@paramsRequired(["newPassword", "token"])
def reset_password_using_token_completion():
    """ Finaliza a redefinição de senha """

    newPassword = request.form["newPassword"]
    if len(newPassword) < 6:
        return jsonify({
            "icon": "error",
            "title": "Oops",
            "text": "Sua nova senha deve possuir no mínimo 6 caracteres"
        }), 200
    
    user:PainelUsers = PainelUsers.query.filter_by(token_redefinition_password=request.form['token']).first()
    if not user:
        return jsonify({
            "icon": "error",
            "title": "Oops",
            "text": "O link que você abriu é inválido. Gere um novo link de redefinição."
        }), 200
    
    user.password = hash_pass(newPassword)
    user.token_redefinition_password = None
    db.session.commit()
        
    return jsonify({
        "icon": "success",
        "title": "Sucesso",
        "text": "A sua senha foi atualizada com sucesso! Faça login para continuar"
    }), 200


@auth.route("/reset/password/otp/send", methods=["POST"])
@paramsRequired(["emailOTP"])
def send_otp_code():
    """ Envia o código de redefinição para o email do usuário """
    
    user:PainelUsers = PainelUsers.query.filter_by(email=request.form["emailOTP"]).first()
    if not user:
        return jsonify({
            "icon": "error",
            "title": "Oops",
            "text": "O usuário não foi encontrado no sistema. Realize o seu cadastro"
        }), 200
    
    generated_token = send_mail_reset(user.email, user.name)
    if generated_token:
        user.token_redefinition_password = generated_token
        db.session.commit()
        return jsonify({
            "icon": "success",
            "title": "Link enviado",
            "text": "O link de redefinição foi enviado para o seu email"
        }), 200


    return jsonify({
        "icon": "error",
        "title": "Oops",
        "text": "Um erro ocorreu ao enviar a solicitação de redefinição de senha"
    }), 200
