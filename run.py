from flask import Flask
from src.config.data_base import init_db, db
from src.routes import init_routes
from src.Infrastructure.Model.user import User  # importa modelos para criar tabelas

def create_app():
    """
    Cria e configura a aplicação Flask.
    """
    app = Flask(__name__)
    init_db(app)
    init_routes(app)

    # Cria as tabelas novas
    with app.app_context():
        db.create_all()
        print("Tabelas criadas!")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Porta 5000 e debug ativo
