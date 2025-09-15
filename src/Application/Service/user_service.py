from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Infrastructure.http.whats_app import WhatsAppService

import os

from dotenv import load_dotenv

load_dotenv()  

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp_number = os.getenv("TWILIO_PHONE_NUMBER")


class UserService:
    @staticmethod
    def create_user(name, email, password, cnpj, celular):
        ddd = 55
        numero_formatado = f'whatsapp:+{ddd}{celular}'
        whats_service = WhatsAppService(account_sid, auth_token, from_whatsapp_number)
        codigo = whats_service.enviar_codigo(numero_formatado)

    
        new_user = UserDomain(name, email, password, cnpj, celular, codigo_validacao=codigo, status=False)
        user = User(
            name=new_user.name,
            email=new_user.email,
            password=new_user.password,
            cnpj=new_user.cnpj,
            celular=new_user.celular,
            codigo_validacao=new_user.codigo_validacao,
            status=False
        )


       
        db.session.add(user)
        db.session.commit()
        return user
    

    @staticmethod
    def validar_codigo(id, codigo_digitado):
        user = User.query.filter_by(id = id).first()
        if not user:
            return False
        
        if user.codigo_validacao == codigo_digitado:
            user.status = True
            user.codigo_validacao = None
            db.session.commit()
            return True
        return False


       
    @staticmethod
    def verifica_user(email, password):
        user = User.query.filter_by(email= email, password= password).first()
        if not user:
            return "Usuário não encontrado"
        
        if not user.status:
                return "Usuário não validado"
        
        if user.password != password:
            return "Senha incorreta"
        
        return "Usuário verificado com sucesso"
    
    @staticmethod
    def put_user(id, name = None, email = None, password = None, cnpj = None, celular = None):
        user = User.query.filter_by(id = id).first()

        if name:
            user.name = name
        if email:
            user.email = email
        if password is not None:
            user.password = password
        if cnpj:
            user.cnpj = cnpj
        if celular:
            user.celular = celular

        db.session.commit()
        return user.to_dict()
            
    @staticmethod
    def resgata_user(id):
        user = User.query.filter_by(id = id).first()
        if not user:
            return None
        else:
            return user.to_dict()

    @staticmethod
    def deletar_user(id):
        user = User.query.filter_by(id = id).first()
        if not user:
            return None
        else:
            db.session.delete(user)
            db.session.commit()