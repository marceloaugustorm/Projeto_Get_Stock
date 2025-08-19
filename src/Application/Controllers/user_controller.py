from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        cnpj = data.get('cnpj')
        celular = data.get('celular')


        if not name or not email or not password or not cnpj or not celular:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(name, email, password, cnpj, celular)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)
    
    @staticmethod
    def verifica_user():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = UserService.verifica_user(email, password)

        if user:
            return jsonify({"message": "Bem vindo"})
        
        if not user:
            return jsonify({"message": "Usuário ou senha Invalidos"})
        
