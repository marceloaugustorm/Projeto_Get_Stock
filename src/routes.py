from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response

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
    def get(id):
        return UserController.get_user(id)
    
    @app.route('/verifica', methods=['POST'])
    def verify():
        return UserController.verify_user()
    
    
    @app.route('/user/<int:id>',methods = ['PUT'])
    def put(id):
        return UserController.atualiza_user(id)
    
    @app.route('/verifica/code', methods = ['POST'])
    def validation_code():
        return UserController.validate_code()

    @app.route('/user/<int:id>', methods = ['DELETE'])
    def delete(id):
        return UserController.deletando_user(id)

