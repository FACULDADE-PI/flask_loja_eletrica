from urllib.parse import quote
from os import environ
from dotenv import load_dotenv

# Carrega o dotenv
load_dotenv()

# CONEXOES DE DATABASE
DATABASE_PAINEL = {
    "HOST": quote(environ['DB_PAINEL_HOST']),
    "USER": quote(environ['DB_PAINEL_USER']),
    "PASSWORD": quote(environ['DB_PAINEL_PASS']),
    "DATABASE": quote(environ['DB_PAINEL_NAME']) 
}

# SQLALCHEMY CONFIGS
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_PAINEL["USER"]}:{DATABASE_PAINEL["PASSWORD"]}@{DATABASE_PAINEL["HOST"]}/{DATABASE_PAINEL["DATABASE"]}?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 3,
    'pool_recycle': 15,
    'pool_pre_ping': True
}

# secret key para as sessões
SECRET_KEY = environ['SECRET_KEY']

# CONFIGURAÇÕES DO JSON PARA UTF-8
JSON_AS_ASCII = False
JSONIFY_PRETTYPRINT_REGULAR = True

# CONFIGURAÇÕES DE EMAIL
MAIL_PORT = 465
MAIL_SERVER = "smtp.gmail.com"
MAIL_USE_TLS = False 
MAIL_USE_SSL = True 
MAIL_USERNAME = environ['GMAIL_EMAIL_USER']
MAIL_PASSWORD = environ['GMAIL_EMAIL_PASS']

# REDEFINIÇÃO DE SENHA
EXPIRATION_TOKEN = 60 # em minutos
TOKEN_SALT = SECRET_KEY

# JINJA2
TEMPLATES_AUTO_RELOAD = True
