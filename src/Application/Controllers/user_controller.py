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
    def validate_code():
        data = request.get_json()
        id = data.get('id')
        codigo_digitado = data.get('codigo_digitado')

        user = UserService.validar_codigo(id, codigo_digitado)

        if user:
            return jsonify({"message": "Usuário Validado"})
        else:
            return jsonify({"message": "Código Inválido"})
    
    @staticmethod
    def get_user(id):
        user = UserService.resgata_user(id)
        if not user:
            return(jsonify({"message": "Usuário não encontrado"}))
        return (jsonify({"Usuário encontrado": user}))

    
    @staticmethod
    def verify_user():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email e senha são obrigatórios"})

        resultado = UserService.verifica_user(email, password)
        return jsonify({"message": resultado})
        
    
    @staticmethod
    def atualiza_user(id):
        data = request.get_json()

        user = UserService.put_user(
            id,
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'),
            cnpj=data.get('cnpj'),
            celular=data.get('celular')
        )

        if not user:
            return jsonify({"message": "Usuário não encontrado"}), 404
        
        return jsonify({"message": "Usuário Atualizado", "user": user}), 200

    @staticmethod
    def deletando_user(id):
        data = request.get_json()

        user = UserService.deletar_user(id)

        if not user:
            return jsonify({"message": "O Usuário foi deletado corretamente"}), 404

        return jsonify({"message": "Usuário não deletado"})
             



        
