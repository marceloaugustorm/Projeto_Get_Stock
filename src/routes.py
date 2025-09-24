from src.Application.Controllers.user_controller import UserController
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