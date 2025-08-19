class UserDomain:
    def __init__(self, name, email, password, cnpj, celular, status):
        self.name = name
        self.email = email
        self.password = password
        self.cnpj = cnpj
        self.celular = celular
        self.status = status
        
    
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "cnpj": self.cnpj,
            "celular": self.celular,
            "status": self.status
        }
