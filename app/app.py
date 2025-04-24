from flask import Flask, render_template
from app.database import db
from flask_migrate import Migrate
from datetime import datetime  # <-- precisa importar

from app.routers.usuarios import bp_usuarios

def create_app():
    app = Flask(__name__)
    
    # Configurações
    conexao = 'sqlite:///meubanco.sqlite'
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = conexao
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Extensões
    db.init_app(app)
    migrate = Migrate(app, db)
    
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    # Blueprints
    app.register_blueprint(bp_usuarios)
    return app
