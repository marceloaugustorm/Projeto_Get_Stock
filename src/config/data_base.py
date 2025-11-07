import os
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    Suporta PostgreSQL (como Supabase) e SQLite local.
    """

    # Se existir variável de ambiente DATABASE_URL, usa ela (Supabase)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Caso use senha com caracteres especiais, encode
        parts = database_url.split("@")
        if len(parts) == 2 and ":" in parts[0]:
            user_pass, host_port_db = parts
            user, password = user_pass.split(":", 1)
            password = quote_plus(password)  # codifica caracteres especiais
            database_url = f"{user}:{password}@{host_port_db}"

        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database_url}"
    else:
        # Banco SQLite local (fallback)
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, "market_management.db")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
