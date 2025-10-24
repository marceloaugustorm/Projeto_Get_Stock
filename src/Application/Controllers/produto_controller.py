from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from src.Infrastructure.Model.produto import Produto
from src.Application.Service.produto_service import ProdutoService
import os


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
        
        return jsonify({"message": "Produtos não encontrados"})
    

    @staticmethod
    def att_produto(id):
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        quantidade = request.form.get("quantidade")
        imagem = request.files.get("imagem")
        
        if not any([nome, preco, quantidade, imagem]):
            return jsonify({"erro": "Campos obrigatórios faltando."}), 400
        
        produtos = ProdutoService.atualizar_produtos(id, nome, preco, quantidade, imagem)

        if produtos:
            return jsonify(produtos.to_dict_product())
        
        return jsonify({"message": "Erro ao atualizar produto"})
    

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




