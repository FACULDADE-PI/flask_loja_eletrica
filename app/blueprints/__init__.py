from flask.blueprints import Blueprint


client = Blueprint(
    name = 'user', 
    import_name = __name__, 
    url_prefix='/user'
)

auth = Blueprint(
    name = 'auth', 
    import_name = __name__, 
    url_prefix='/auth'
)

admin = Blueprint(
    name = 'admin', 
    import_name = __name__, 
    url_prefix='/admin'
)