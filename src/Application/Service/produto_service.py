from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.venda import Venda
from werkzeug.utils import secure_filename
from src.config.data_base import db
import pandas as pd
import os


class ProdutoService:
    @staticmethod
    def criar_produto(nome, preco, quantidade, status, imagem):

        if not nome or not preco or not quantidade:
            raise ValueError("Campos obrigatórios ausentes (nome, preco ou quantidade)")

        try:
            preco_original = preco
            quantidade_original = quantidade
            status_original = status

            preco = float(preco)
            quantidade = int(quantidade)

    
            if isinstance(status, str):
                status = status.lower() in ['true', '1', 't', 'yes']
            else:
                status = bool(status)

            print(f"Convertidos: preco={preco} (de {preco_original}), quantidade={quantidade} (de {quantidade_original}), status={status} (de {status_original})")

        except ValueError as e:
            raise ValueError(f"Erro de conversão de tipos: {e}")

        if imagem:
            print(f"Caminho da imagem recebido: {imagem}")
        else:
            print("Nenhuma imagem enviada.")

        new_produto = ProdutoDomain(nome, preco, quantidade, status, imagem)
        print("✅ ProdutoDomain criado com sucesso.")

        
        produto = Produto(
            nome=new_produto.nome,
            preco=new_produto.preco,
            quantidade=new_produto.quantidade,
            status=new_produto.status,
            imagem=new_produto.imagem
        )
        print("✅ Produto (Model) instanciado com sucesso.")

        try:
            db.session.add(produto)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

            raise e

        return produto


    
    @staticmethod
    def obter_dados_dashboard():
        """Combina dados de produtos e vendas para o dashboard"""

        produtos = Produto.query.all()
        if not produtos:
            return None

        df_produtos = pd.DataFrame([p.to_dict_product() for p in produtos])

        vendas = Venda.query.all()
        if vendas:
            df_vendas = pd.DataFrame([v.to_dict_venda() for v in vendas])
        else:
            df_vendas = pd.DataFrame(columns=["id_produto", "quantidade", "valor_total"])

        # 🔹 Métricas de vendas
        total_vendas = df_vendas["valor_total"].sum() if not df_vendas.empty else 0
        produtos_vendidos = (
            df_vendas.groupby("id_produto")["quantidade"].sum().reset_index()
            if not df_vendas.empty
            else pd.DataFrame(columns=["id_produto", "quantidade"])
        )

        ranking = []
        if not produtos_vendidos.empty:
            ranking = produtos_vendidos.sort_values(by="quantidade", ascending=False).head(5).to_dict(orient="records")

        return {
            "produtos": df_produtos,
            "vendas": df_vendas,
            "total_vendas": total_vendas,
            "ranking": ranking
        }

    @staticmethod
    def listar_produtos():
        return Produto.query.filter_by(status=True).all()

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

