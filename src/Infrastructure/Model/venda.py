from src.config.data_base import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # ← ADICIONE
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)  # ← Opcional mas útil

    produto = db.relationship('Produto', back_populates='vendas_relacionadas')
    usuario = db.relationship('User', backref='vendas')  # ← ADICIONE

    def to_dict_venda(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "quantidade_vendida": self.quantidade,
            "preco_no_momento": self.preco_unitario,
            "preco_total": self.preco_total,
            "produto_nome": self.produto.nome if self.produto else None,
            "user_id": self.user_id,  # ← Opcional
            "data_venda": self.data_venda.isoformat() if self.data_venda else None  # ← Opcional
        }