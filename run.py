from flask import Flask
from src.config.data_base import init_db, db
from src.routes import init_routes
from src.Infrastructure.Model.user import User  # importa os modelos para criar as tabelas

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    init_db(app)

    init_routes(app)

    # Cria as tabelas
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
