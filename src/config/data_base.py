import os
from flask_sqlalchemy import SQLAlchemy
import socket

# Opcional: força IPv4
original_getaddrinfo = socket.getaddrinfo
def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = patched_getaddrinfo

db = SQLAlchemy()

def init_db(app):
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 3600,
            'pool_size': 5,
            'max_overflow': 10,
            'connect_args': {'connect_timeout': 10}
        }
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, "market_management.db")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
