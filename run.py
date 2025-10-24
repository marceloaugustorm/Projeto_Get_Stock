from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.config.data_base import init_db, db
from src.routes import init_routes
from src.Infrastructure.Model.user import User
import os

def create_app():
    """
    Cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    # ✅ CORS configurado com seu frontend Vercel
    allowed_origins = [
        "http://localhost:3000",
        "https://get-stock-front.vercel.app",  # ✅ Seu frontend
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ]
    
    CORS(app, resources={
        r"/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True  # ✅ Para cookies/JWT
        }
    })
    
    # JWT Secret do ambiente ou padrão
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "flaroque")
    jwt = JWTManager(app)

    # Inicializar banco e rotas
    init_db(app)
    init_routes(app)

    # Rota raiz - Health Check
    @app.route('/')
    def home():
        return jsonify({
            "message": "API GetStock está funcionando!",
            "status": "online",
            "version": "1.0.0",
            "frontend": "https://get-stock-front.vercel.app"
        }), 200

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"}), 200

    # Criar tabelas
    with app.app_context():
        db.create_all()
        print("Tabelas criadas!")

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)