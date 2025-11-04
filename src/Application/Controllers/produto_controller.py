from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
        
        return jsonify({"message": "Produtos não encontrados"}), 404
    

    @staticmethod
    def att_produto(id):
        data = request.get_json()
        nome = data.get("nome")
        preco = data.get("preco")
        quantidade = data.get("quantidade")

        produto = ProdutoService.atualizar_produtos(
            id, nome=nome, preco=preco, quantidade=quantidade
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
