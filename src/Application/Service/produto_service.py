from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.venda import Venda
from werkzeug.utils import secure_filename
from src.config.data_base import db
import os


class ProdutoService:
    @staticmethod
    def criar_produto(nome, preco, quantidade, status, imagem):
        new_produto = ProdutoDomain(nome, preco, quantidade, status, imagem)

        produto = Produto(
            nome=new_produto.nome,
            preco=new_produto.preco,
            quantidade=new_produto.quantidade,
            status=new_produto.status,
            imagem=new_produto.imagem
        )

        db.session.add(produto)
        db.session.commit()
        return produto

    @staticmethod
    def listar_produtos():
        return db.session.query(Produto).all()

    @staticmethod
    def atualizar_produtos(id, nome=None, preco=None, quantidade=None, imagem=None):
        new_produto = Produto.query.filter_by(id=id).first()
        
        if not new_produto:
            return None  

        if nome:
            new_produto.nome = nome
        if preco:
            new_produto.preco = preco
        if quantidade:
            new_produto.quantidade = quantidade
        if imagem:
            if hasattr(imagem, 'filename'):  # Se for um arquivo
                filename = secure_filename(imagem.filename)
                filepath = os.path.join('static/uploads', filename)
                imagem.save(filepath)
                new_produto.imagem = filepath
            else:
                new_produto.imagem = imagem

        db.session.commit()
        return new_produto

    @staticmethod
    def inativar_produto(id):
        produto = Produto.query.filter_by(id=id).first()
    
        if not produto:
            return None
    
        produto.status = False  
        db.session.commit()
        return produto

    @staticmethod
    def ativar_produto(id):
        produto = Produto.query.filter_by(id=id).first()
        
        if not produto:
            return None
        
        produto.status = True  
        db.session.commit()
        return produto

    @staticmethod
    def excluir_produto(id):
        produto = Produto.query.filter_by(id=id).first()

        if not produto:
            return None
        
        db.session.delete(produto)
        db.session.commit()
        return True

    @staticmethod
    def vender_produto(id, quantidade_venda):
        produto = Produto.query.filter_by(id=id).first()
        
        if not produto:
            return None, "Produto não encontrado"

        if not produto.status:
            return None, "Produto inativo!"

        if produto.quantidade < quantidade_venda:
            return None, "Estoque insuficiente!"

        # Diminui o estoque
        produto.quantidade -= quantidade_venda

        # Cria registro da venda
        nova_venda = Venda(
            produto_id=produto.id,
            quantidade=quantidade_venda,
            preco_unitario=produto.preco,
            preco_total=produto.preco * quantidade_venda
        )

        db.session.add(nova_venda)
        db.session.commit()

        return nova_venda, None
