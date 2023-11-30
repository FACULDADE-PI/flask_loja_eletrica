from app import db

class TypeUsers(db.Model):
    __tablename__ = "type_users"
    
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slug = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False) 
    active = db.Column(db.Boolean, default=True)


    def __init__(self, description, slug, active):
        self.slug = slug
        self.description = description
        self.active = active

    def __repr__(self) -> str:
        return str(self.slug)
