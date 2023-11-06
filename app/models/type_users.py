from app import db

class TypeUsers(db.Model):
    __tablename__ = "type_users"
    
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(100), nullable=False)

    def __init__(self, desc):
        self.desc = desc

    def __repr__(self) -> str:
        return str(self.desc)
