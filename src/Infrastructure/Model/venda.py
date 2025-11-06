from src.config.data_base import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)

    # Relacionamento
    produto = db.relationship('Produto', backref='vendas')

    def to_dict_venda(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "quantidade_vendida": self.quantidade,
            "preco_no_momento": self.preco_unitario,
            "preco_total": self.preco_total,
            "produto_nome": self.produto.nome if self.produto else None
        }
