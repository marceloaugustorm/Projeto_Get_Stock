from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 

class UserService:
    @staticmethod
    def create_user(name, email, password, cnpj, celular):
        new_user = UserDomain(name, email, password, cnpj, celular, status = False)
        user = User(name=new_user.name, email=new_user.email, password=new_user.password, cnpj = new_user.cnpj, celular = new_user.celular, status = False)        
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def verifica_user(email, password):
        user = User.query.filter_by(email= email, password= password).first()
        if not user:
            return None
        else:
            if user:
                return("Bem - Vindo")
