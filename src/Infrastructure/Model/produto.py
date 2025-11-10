from src.config.data_base import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Boolean, default=True, nullable=True)
    imagem = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 


    vendas_relacionadas = db.relationship('Venda', back_populates='produto')

    def to_dict_product(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "status": self.status,
            "imagem": self.imagem,
            "user_id": self.user_id
        }