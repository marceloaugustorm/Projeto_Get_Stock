import os
import socket
from flask_sqlalchemy import SQLAlchemy

# ===== PATCH IPv4 - RESOLVE PROBLEMA DE CONEXÃO COM SUPABASE =====
original_getaddrinfo = socket.getaddrinfo

def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    """Força resolução DNS para IPv4 apenas"""
    return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

socket.getaddrinfo = patched_getaddrinfo
# ==================================================================

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    Suporta PostgreSQL (Supabase) e fallback SQLite local.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Usa porta 6543 (connection pooler) se estiver usando porta 5432
        if ":5432/" in database_url:
            database_url = database_url.replace(":5432/", ":6543/")
        
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        
        # Configurações otimizadas para PostgreSQL/Supabase
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 3600,
            'pool_size': 5,
            'max_overflow': 10,
            'connect_args': {
                'connect_timeout': 10
            }
        }
    else:
        # Fallback para SQLite local
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, "market_management.db")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)