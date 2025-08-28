from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Infrastructure.http.whats_app import WhatsAppService


account_sid = "AC739251f716815e12764015f1808d1ce1"
auth_token = "ee5e1a42f8a3549627981dd568cf2c95"
from_whatsapp_number = "whatsapp:+14155238886" 

class UserService:
    @staticmethod
    def create_user(name, email, password, cnpj, celular):
        whats_service = WhatsAppService(account_sid, auth_token, from_whatsapp_number)
        codigo = whats_service.enviar_codigo(celular)

        new_user = UserDomain(name, email, password, cnpj, celular, status = False)
        user = User(
            name=new_user.name, 
            email=new_user.email, 
            password=new_user.password, 
            cnpj = new_user.cnpj, 
            celular = new_user.celular, 
            codigo_validacao = codigo, 
            status = "DESATIVADO"
            )


       
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def validar_codigo(codigo_digitado, celular):
        user = User.query.filter_by(celular=celular).first()
        if not user:
            return False
        
        if user.codigo_validacao == codigo_digitado:
            user.status = "ATIVO"
            db.session.commit()
            return True
        return False

       
    @staticmethod
    def verifica_user(email, password):
        user = User.query.filter_by(email= email, password= password).first()
        if not user:
            return None
        else:
            if user:
                return("Bem - Vindo")
    
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

