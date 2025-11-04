from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.produto_controller import ProdutoController
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/user/<int:id>', methods = ['GET'])
    @jwt_required()
    def get(id):
        return UserController.get_user(id)
    
    @app.route('/verifica', methods=['POST'])
    def verify():
        return UserController.verify_user()
    
    
    @app.route('/user/<int:id>',methods = ['PUT'])
    @jwt_required()
    def put(id):
        return UserController.atualiza_user(id)
    
    @app.route('/verifica/code', methods = ['POST'])
    def validation_code():
        return UserController.validate_code()

    @app.route('/user/<int:id>', methods = ['DELETE'])
    @jwt_required()
    def delete(id):
        return UserController.delete_user(id)
    
    @app.route('/produto', methods = ['POST'])
    @jwt_required()
    def criar_produto():
        return ProdutoController.register_produto()
    
    @app.route('/produto', methods = ['GET'])
    @jwt_required()
    def listar_produto():
        return ProdutoController.list_product()
    

    @app.route('/produto/<int:id>', methods = ['PUT'])
    @jwt_required()
    def att_produto(id):
        return ProdutoController.att_produto(id)
    

    @app.route('/ativar/<int:id>', methods = ['PATCH'])
    @jwt_required()
    def ativar_product(id):
        return ProdutoController.ativar_produto(id)
    
    @app.route('/desativar/<int:id>', methods = ['PATCH'])
    @jwt_required()
    def desativar_product(id):
        return ProdutoController.inativar_produto(id)
    

    @app.route('/produto/<int:id>', methods = ['DELETE'])
    @jwt_required()
    def exclusao_produto(id):
        return ProdutoController.deletar_produto(id)
    
    @app.route('/produto/<int:id>/vender', methods=['PATCH'])
    @jwt_required()
    def vender_produto(id):
        return ProdutoController.vender(id)
