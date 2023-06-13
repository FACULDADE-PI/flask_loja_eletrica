from app import db
from flask_login import UserMixin
from app.utils import hash_pass, current_time



class Users(UserMixin, db.Model):
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=True)
    type_user = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=False)


    def __init__(self, email, password, name):
        self.email = email
        self.password = hash_pass(password)
        self.name = name
        self.date_joined = current_time()
        self.type_user = 1 # usuário
        self.active = 1 # não precisa validar

    def __repr__(self) -> str:
        return str(self.name)
