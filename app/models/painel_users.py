from app import db, login_manager
from flask_login import UserMixin
from app.utils import hash_pass, current_time
from .type_users import TypeUsers


class PainelUsers(UserMixin, db.Model):
    __tablename__ = "painel_users"
    
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    token_redefinition_password = db.Column(db.String(256), unique=True, nullable=True)
    date_joined = db.Column(db.DateTime, nullable=True)
    type_user = db.Column(db.ForeignKey("type_users.Id"), default=5)

    active = db.Column(db.Boolean, default=False)


    def get_id(self):
        return str(self.Id)

    def __init__(self, email, password, name, active):
        self.email = email
        self.password = hash_pass(password)
        self.name = name
        self.date_joined = current_time()
        self.type_user = TypeUsers.query.filter_by(slug="Usuário").first().Id
        self.active = active

    def __repr__(self) -> str:
        return str(self.Id)



@login_manager.user_loader
def user_loader(Id):
    return PainelUsers.query.filter_by(Id=Id).first()


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = PainelUsers.query.filter_by(email=email).first()
    return user if user else None
