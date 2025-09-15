from flask import Flask
from flask_jwt_extended import JWTManager
from src.config.data_base import init_db, db
from src.routes import init_routes
from src.Infrastructure.Model.user import User  

def create_app():
    """
    Cria e configura a aplicação Flask.
    """
    app = Flask(__name__)
    
    # Configura o JWT
    app.config["JWT_SECRET_KEY"] = "flaroque"  
    jwt = JWTManager(app)  


    init_db(app)
    init_routes(app)

    with app.app_context():
        db.create_all()
        print("Tabelas criadas!")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)