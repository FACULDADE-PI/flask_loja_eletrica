from flask.blueprints import Blueprint


# @administrativo
auth = Blueprint(
    name = 'auth', 
    import_name = __name__, 
    url_prefix='/auth'
)