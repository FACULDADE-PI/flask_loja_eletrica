from app import db
from flask_login import UserMixin


class AddressScanned(UserMixin, db.Model):
    __tablename__ = "address_scanned"
    
    quem_lancou = db.Column(db.ForeignKey("painel_users.Id"), default=3)
    
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cep = db.Column(db.String(100), nullable=False)
    rua = db.Column(db.String(128), unique=False, nullable=False)
    numero = db.Column(db.String(128), nullable=False)
    estado = db.Column(db.String(128), nullable=False)

    long = db.Column(db.String(128), nullable=False)
    lat = db.Column(db.String(128), nullable=False)

    bairro = db.Column(db.String(256), unique=False, nullable=False)
    cidade = db.Column(db.String(256))

    data_lancamento = db.Column(db.DateTime, nullable=False)
    data_entrega = db.Column(db.DateTime, nullable=True)

    entregue = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self) -> str:
        return str(self.Id)

    def __init__(self, cep, rua, numero, bairro, quem_lancou, cidade, data_lancamento, data_entrega, long, lat, entregue, active, estado):
        self.cep = cep
        self.rua = rua
        self.long = long
        self.estado = estado
        self.lat = lat
        self.entregue = entregue
        self.numero = numero
        self.bairro = bairro
        self.quem_lancou = quem_lancou
        self.cidade = cidade
        self.data_lancamento = data_lancamento
        self.data_entrega = data_entrega
        self.active = active

    def get_id(self):
        return str(self.Id)


