from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from os.path import dirname, abspath

# path do arquivo raiz
path = dirname(abspath(__file__)).replace("\\", "/")
path = path.rsplit("/", 1)[0]

# Flask application -> Configura uma aplicação flask
# Docs: https://flask-ptbr.readthedocs.io/en/latest/
app:Flask = Flask(__name__)
app.config.from_pyfile(path + "/config.py")

# DB Connection -> Gerencia conexão com o banco de dados
# Docs: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
db:SQLAlchemy = SQLAlchemy(app)

#Flask Migrate -> Usado para atualizar estrutura do banco de dados com base nos models
migrate = Migrate(app,db)

# Faz importação das rotas e models e blueprints
from app.routes import *
from app.blueprints import *

# Creating blueprint and registering
# Docs: https://flask.palletsprojects.com/en/2.2.x/tutorial/views/
app.register_blueprint(auth)

# Clear Caching Chrome -> Remove o cache criado pelo navegador após a requisição
@app.after_request
def debug_after(response):
    """ Remove o lixo do cache criado pelo Chrome """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers['Connection'] = 'close'  
    return response
