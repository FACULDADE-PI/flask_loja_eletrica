# -*- coding: utf-8 -*-
from flask import jsonify
from functools import wraps
from flask import request


def paramsRequired(parameters:list):
    """ Avalia se todos os parâmetros foram recebidos """

    def decoratorType(func):

        @wraps(func)
        def wrapper(*args,**kwargs):
            missing = []

            for parameter in parameters:
                if not type(request.form.get(parameter)) != type(None) and not type(request.args.get(parameter)) != type(None) and not type(kwargs.get(parameter)) != type(None):
                    missing.append(parameter)


            if len(missing) > 0:
                return jsonify({
                    'title': 'Error',
                    'text': 'Existem parâmetros faltando na requisição',
                    'icon': 'error',
                }), 200
                                
            return func(*args,**kwargs)

        return wrapper
    
    return decoratorType


    