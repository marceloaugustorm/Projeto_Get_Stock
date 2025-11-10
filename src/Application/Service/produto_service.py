from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.venda import Venda
from werkzeug.utils import secure_filename
from src.config.data_base import db
import pandas as pd
import os


class ProdutoService:
    @staticmethod
    def criar_produto(nome, preco, quantidade, status, imagem_url, user_id):  # ← Adicione user_id
        """
        Cria um novo produto vinculado ao usuário.
        """
        try:
            produto = Produto(
                nome=nome,
                preco=preco,
                quantidade=quantidade,
                status=status,
                imagem=imagem_url,
                user_id=user_id  # ← ADICIONE ESTA LINHA
            )
            
            db.session.add(produto)
            db.session.commit()
            
            return produto
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar produto: {str(e)}")

        
    @staticmethod
    def obter_dados_dashboard(user_id=None):
        """Combina dados de produtos e vendas para o dashboard, filtrado por usuário"""

        # Filtra produtos por usuário
        if user_id:
            produtos = Produto.query.filter_by(user_id=user_id).all()
        else:
            produtos = Produto.query.all()
        
        if not produtos:
            return None
        
        df_produtos = pd.DataFrame([p.to_dict_product() for p in produtos])

        # Filtra vendas por usuário
        if user_id:
            vendas = Venda.query.filter_by(user_id=user_id).all()
        else:
            vendas = Venda.query.all()
        
        if vendas:
            df_vendas = pd.DataFrame([v.to_dict_venda() for v in vendas])
        else:
            df_vendas = pd.DataFrame(columns=["produto_id", "quantidade_vendida", "preco_total"])

        # Métricas de vendas
        total_vendas = df_vendas["preco_total"].sum() if not df_vendas.empty else 0
        produtos_vendidos = (
            df_vendas.groupby("produto_id")["quantidade_vendida"].sum().reset_index()
            if not df_vendas.empty
            else pd.DataFrame(columns=["produto_id", "quantidade_vendida"])
        )

        ranking = []
        if not produtos_vendidos.empty:
            ranking = produtos_vendidos.sort_values(by="quantidade_vendida", ascending=False).head(5).to_dict(orient="records")

        return {
            "produtos": df_produtos,
            "vendas": df_vendas,
            "total_vendas": total_vendas,
            "ranking": ranking
        }

    @staticmethod
    def listar_produtos(user_id=None):
        """
        Lista produtos ativos, opcionalmente filtrados por usuário.
        """
        query = Produto.query.filter_by(status=True)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        return query.all()

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
        produto = Produto.query.get(id)
        if not produto:
            return None
        
        # Soft delete
        produto.status = False
        db.session.commit()
        return produto

    @staticmethod
    def vender_produto(id, quantidade_venda):
        produto = Produto.query.filter_by(id=id).first()

        if not produto:
            return None, "Produto não encontrado"

        if not produto.status:
            return None, "Produto inativo"

        try:
            quantidade_venda = int(quantidade_venda)
        except ValueError:
            return None, "Quantidade inválida"

        if produto.quantidade < quantidade_venda:
            return None, "Estoque insuficiente"

        produto.quantidade -= quantidade_venda

        nova_venda = Venda(
            produto_id=produto.id,
            quantidade=quantidade_venda,
            preco_unitario=produto.preco,
            preco_total=produto.preco * quantidade_venda
        )

        db.session.add(nova_venda)
        db.session.commit()

        return nova_venda, None

