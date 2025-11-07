import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    Suporta PostgreSQL (Supabase) e fallback SQLite local.
    """
    # Usa variável de ambiente DATABASE_URL ou fallback local
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        import os
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, "market_management.db")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
