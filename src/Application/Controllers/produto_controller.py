from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.Infrastructure.Model.produto import Produto
from src.Application.Service.produto_service import ProdutoService
import os
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt

class ProdutoController:
    @staticmethod
    def register_produto():
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        quantidade = request.form.get("quantidade")
        status = request.form.get("status")
        imagem = request.files.get("imagem")
        
        if not all([nome, preco, quantidade]):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400

        upload_folder = os.path.join(current_app.root_path, "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        imagem_path = None
        if imagem:
            filename = imagem.filename
            save_path = os.path.join(upload_folder, filename)
            imagem.save(save_path)
            imagem_path = os.path.join("static", "uploads", filename)

        produto = ProdutoService.criar_produto(nome, preco, quantidade, status, imagem_path)

        return jsonify({
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": produto.quantidade,
            "status": produto.status,
            "imagem": produto.imagem
        }), 201
    

    @staticmethod
    def list_product():
        produtos = ProdutoService.listar_produtos()

        if produtos:
            return jsonify([produto.to_dict_product() for produto in produtos])
        
        return jsonify({"message": "Produtos não encontrados"}), 404
    

    @staticmethod
    def att_produto(id):
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        quantidade = request.form.get("quantidade")
        imagem = request.files.get("imagem")

        produto = ProdutoService.atualizar_produtos(
            id, nome=nome, preco=preco, quantidade=quantidade, imagem=imagem
        )

        if not produto:
            return jsonify({"erro": "Produto não encontrado"}), 404
        
        return jsonify(produto.to_dict_product()), 200


    @staticmethod
    def vender(id):
    """Registrar uma venda de produto"""
    data = request.get_json()
    quantidade_venda = int(data.get("quantidade_venda", 1))

    venda, erro = ProdutoService.vender_produto(id, quantidade_venda)

    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify({
        "mensagem": "Venda registrada com sucesso!",
        "venda": venda.to_dict_venda()
    }), 201
    

    @staticmethod
    def inativar_produto(id):
        """Inativar produto"""
        produto = ProdutoService.inativar_produto(id)
        
        if produto:
            return jsonify({
                "message": "Produto inativado com sucesso!",
                "produto": produto.to_dict_product()
            }), 200
        
        return jsonify({"erro": "Produto não encontrado"}), 404
    

    @staticmethod
    def ativar_produto(id):
        """Ativar produto"""
        produto = ProdutoService.ativar_produto(id)
        
        if produto:
            return jsonify({
                "message": "Produto ativado com sucesso!",
                "produto": produto.to_dict_product()
            }), 200
        
        return jsonify({"erro": "Produto não encontrado"}), 404
    

    @staticmethod
    def deletar_produto(id):
        produto = ProdutoService.excluir_produto(id)

        if produto:
            return jsonify({"message": "Produto excluído com sucesso"}), 200
        
        return jsonify({"message": "Erro ao excluir produto"}), 404

   @staticmethod
def dashboard():
    """Dashboard analítico de produtos"""
    produtos = ProdutoService.listar_produtos()
    if not produtos:
        return jsonify({"erro": "Nenhum produto encontrado"}), 404

    df = pd.DataFrame([p.to_dict_product() for p in produtos])

    total_produtos = len(df)
    total_ativos = len(df[df['status'] == 'ativo'])
    total_inativos = len(df[df['status'] == 'inativo'])
    valor_total_estoque = (df['preco'].astype(float) * df['quantidade'].astype(int)).sum()

    plt.figure(figsize=(4, 3))
    df['status'].value_counts().plot(kind='bar', color=['green', 'red'])
    plt.title('Produtos Ativos x Inativos')
    plt.xlabel('Status')
    plt.ylabel('Quantidade')

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    return jsonify({
        "total_produtos": total_produtos,
        "ativos": total_ativos,
        "inativos": total_inativos,
        "valor_total_estoque": round(valor_total_estoque, 2),
        "grafico_status": f"data:image/png;base64,{img_base64}"
    })

