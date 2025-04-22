from flask import Blueprint, render_template, request, flash, redirect
from datetime import datetime


bp_routes = Blueprint('routes', __name__)

@bp_routes.route('/')
@bp_routes.route('/index')
def index():
    return render_template('index.html', now=datetime.now())

@bp_routes.route('/contato')
def contato():
    return render_template('contato.html', now=datetime.now())

@bp_routes.route('/login')
def login():
    return render_template('login.html', now=datetime.now())

@bp_routes.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    if not usuario or not senha:
        flash('Preencha todos os campos')
        return redirect('/login')

    if usuario == 'admin' and senha == '1234':
        return f"usuario: `{usuario}` senha: `{senha}`"
    else:
        flash('Usuário ou senha inválidos')
        return redirect('/login')