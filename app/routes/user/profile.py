from app import db
from app.blueprints import client
from app.models import PainelUsers
from app.utils import verify_pass, hash_pass
from app.middlewares import isAuthenticated, paramsRequired
from flask_login import current_user
from flask import render_template, jsonify, request




@client.route("/profile", methods=["GET"])
@isAuthenticated
def route_profile():
    """ Renderiza a view de login do usuário """
    return render_template("dashboard/pages/user/profile.html", user=current_user)


@client.route("/profile/change", methods=["POST"])
@isAuthenticated
@paramsRequired(["senhaConfirmacao", "novoNome", "novaSenha"])
def route_alterar_profile():
    """ Confere se pode realizar a alteração do perfil e altera """
    user:PainelUsers = PainelUsers.query.filter_by(Id=current_user.Id).first()
    if not verify_pass(request.form['senhaConfirmacao'], user.password):
        return jsonify({
            "icon": "error",
            "title": "Senha incorreta.",
            "text": "A senha de confirmação está incorreta. Corrija os dados de confirmação"
        }), 200
    
    if "$12$" not in request.form["novaSenha"]:
        user.password = hash_pass(request.form['novaSenha'])
    
    user.name = request.form["novoNome"]
    db.session.commit()
    return jsonify({
        "icon": "success",
        "title": "Sucesso!",
        "text": "A alteração do seu perfil foi realizada com sucesso"
    }), 200

