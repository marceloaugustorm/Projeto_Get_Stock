from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa a base de dados com o app Flask e o SQLAlchemy.
    """
    # Troque a URI do MySQL por SQLite:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///market_management.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
