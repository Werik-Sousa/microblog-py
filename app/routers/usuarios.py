from flask import Blueprint, render_template
from app.database import db
from app.models import Usuario
from flask import request, redirect, flash

bp_usuarios = Blueprint('usuarios', __name__)

@bp_usuarios.route('/create')
def create():

    if request.method == 'GET':
        return render_template('usuarios_create.html')

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')

        u = Usuario(nome, email, senha)
        db.session.add(u)
        db.session.commit()
        if not nome or not email or not senha:
            flash('Preencha todos os campos')
            return redirect('/usuarios/create')
        if senha != csenha:
            flash('As senhas não conferem')
            return redirect('/usuarios/create')
        return 'Usuário criado com sucesso!'
    
@bp_usuarios.route('/list')
def list():
    usuarios = Usuario.query.all()
    return render_template('usuarios_list.html', usuarios=usuarios)