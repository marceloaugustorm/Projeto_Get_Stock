from src.config.data_base import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade_vendida = db.Column(db.Integer, nullable=False)
    preco_no_momento = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento
    produto = db.relationship('Produto', backref='vendas')

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "quantidade_vendida": self.quantidade_vendida,
            "preco_no_momento": self.preco_no_momento,
            "data_venda": self.data_venda,
            "produto_nome": self.produto.nome if self.produto else None
        }
