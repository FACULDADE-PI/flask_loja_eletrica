from app import db
from app.blueprints import admin
from app.models import AddressScanned
from app.middlewares import isAuthenticated, hasPrivileges, paramsRequired
from app.utils import current_time
from flask_login import current_user
from flask import render_template, request, jsonify
from requests import get


privilegesEnderecos = ["Administrador", "Supervisor", "Conferente", "Programador"]


@admin.route("/lancar/endereco")
@isAuthenticated
@hasPrivileges(privilegesEnderecos)
def route_lancar_endereco():
    """ Rota de visualizar a tabela de lançamento de endereços """
    enderecos_scaneados = AddressScanned.query.all()
    return render_template("dashboard/pages/administrativo/lancarEnderecos.html", address=enderecos_scaneados, user=current_user)


@admin.route("/editar/endereco", methods=["POST"])
@isAuthenticated
@hasPrivileges(privilegesEnderecos)
def routes_editar_endereco():
    id_registrado = str(request.form.get("id"))

    if id_registrado.isdigit():
        address:AddressScanned = AddressScanned.query.filter_by(AddressScanned.Id==int(id_registrado)).first()
        cep = request.form.get("cep")

        cep = cep.replace("-", "").replace(".", "").replace(" ", "")
        response = get(f"https://cep.awesomeapi.com.br/json/{cep}")
        response = response.json()

        address.cidade = response.get("city")
        address.estado = response.get("state")
        address.rua = response.get("address")
        address.lat = response.get("lat")
        address.long = response.get("lng")
        address.numero = request.form.get("number")
        address.bairro = request.form.get("district")

        db.session.commit()

        return jsonify({
            "icon": "success",
            "title": "Sucesso!",
            "text": "O endereço foi editado com sucesso."
        }), 200
    

    return jsonify({
        "icon": "error",
        "title": "Oops!",
        "text": "O id do endereço é inválido."
    }), 200


@admin.route("/adicionar/endereco", methods=["POST"])
@isAuthenticated
@hasPrivileges(privilegesEnderecos)
def routes_adicionar_endereco():
    """ Adiciona novo endereço """
    cep = request.form.get("cep")

    cep = cep.replace("-", "").replace(".", "").replace(" ", "")
    response = get(f"https://cep.awesomeapi.com.br/json/{cep}")
    response:dict = response.json()

    cidade = response.get("city")
    estado = response.get("state")
    rua = response.get("address")
    lat = response.get("lat")
    long = response.get("lng")
    numero = request.form.get("number")
    bairro = response.get("district")

    address = AddressScanned(
        cep, 
        rua, 
        numero, 
        bairro, 
        current_user.Id, 
        cidade, 
        current_time(), 
        None, 
        long, 
        lat, 
        False, 
        True, 
        estado
    )

    db.session.add(address)
    db.session.commit()

    return jsonify({
        "icon": "success",
        "title": "Sucesso!",
        "text": "O endereço foi salvo com sucesso."
    }), 200




@admin.route("/consultar/cep", methods=["POST"])
def route_retornar_endereco_completo_cep():
    """ Retorna em JSON o endereço """
    cep = request.form.get("cep")
    if not cep:
        return jsonify({}), 404
    
    cep = cep.replace("-", "").replace(".", "").replace(" ", "")
    response = get(f"https://cep.awesomeapi.com.br/json/{cep}")
    return jsonify(response.json()), response.status_code