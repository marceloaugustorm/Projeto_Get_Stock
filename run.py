from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.config.data_base import init_db, db
from src.routes import init_routes
from datetime import timedelta
import os

def create_app():
    """
    Cria e configura a aplicação Flask.
    """
    app = Flask(__name__)

    
    CORS(app, origins=[
        "https://get-stock-front.vercel.app",
        "http://localhost:5173"
    ])

    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "flaroque")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
    jwt = JWTManager(app)

   
    init_db(app)
    init_routes(app)

   
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas!")

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # No ambiente de produção, debug=False
    app.run(debug=os.environ.get("FLASK_DEBUG", "False") == "True", host="0.0.0.0", port=port)
