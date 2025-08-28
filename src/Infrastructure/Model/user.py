from src.config.data_base import db 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    codigo_validacao = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(100), nullable=False)
    


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "cnpj": self.cnpj,
            "celular": self.celular,
            "codigo_validacao": self.codigo_validacao,
            "status": self.status
        }
