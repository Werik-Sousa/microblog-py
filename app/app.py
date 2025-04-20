from flask import Flask, render_template
from app.database import db
from flask_migrate import Migrate

from app.routers.usuarios import bp_usuarios
from app.routers.routes import bp_routes

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

    # Blueprints
    app.register_blueprint(bp_usuarios, url_prefix='/usuarios')
    app.register_blueprint(bp_routes)

    return app