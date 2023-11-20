from app import db
from app.blueprints import auth
from app.models import PainelUsers
from app.utils import verify_pass, hash_pass
from app.middlewares import isAuthenticated, paramsRequired
from flask_login import current_user, UserMixin
from flask import render_template, jsonify, request, redirect




@auth.route("/reset/password", methods=["GET"])
def route_redefinir():
    """ Renderiza a view de redefinir a senha do usuário """
    user:UserMixin = current_user
    if user.is_authenticated:
        return redirect("/")
    
    return render_template("auth/redefinir.html")



@auth.route("/reset/password/otp/send", methods=["POST"])
@paramsRequired(["emailOTP"])
def send_otp_code():
    """ Envia o código de redefinição para o email do usuário """
        

    return jsonify({
        "icon": "success",
        "title": "Link enviado",
        "text": "O link de redefinição foi enviado para o seu email"
    }), 200


