from flask import Blueprint, render_template
from app.database import db
from app.models import Usuario
from datetime import datetime

from flask import request, redirect, flash, url_for

bp_usuarios = Blueprint('usuarios', __name__)

def validar_usuario(nome, email, senha, csenha):
    if not nome or not email or not senha:
        return 'Preencha todos os campos'
    if senha != csenha:
        return 'As senhas não conferem'
    if Usuario.query.filter_by(email=email).first():
        return 'Email já cadastrado'
    return None

@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'GET':
        return render_template('usuarios_create.html', now=datetime.now())

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')

        erro = validar_usuario(nome, email, senha, csenha)
        if erro:
            flash(erro)
            return render_template('usuarios_create.html', nome=nome, email=email, now=datetime.now())

    usuario = Usuario(nome, email, senha)
    db.session.add(usuario)
    db.session.commit()

    flash('Usuário criado com sucesso!')
    return redirect('/login')   

#list    
@bp_usuarios.route('/list')
def list():
    usuarios = Usuario.query.all()
    return render_template('usuarios_list.html', usuarios=usuarios, now=datetime.now())

#update  
@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('usuarios_update', usuario=usuario, now=datetime.now())

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')

        if not nome or not email:
            flash('Preencha todos os campos')
            return redirect(url_for('usuarios.update', id=id))

        usuario.nome = nome
        usuario.email = email
        db.session.commit()
        flash('Dados atualizados com sucesso!')
        return redirect(url_for('usuarios.list'))

#delete
@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('usuarios_delete.html', usuario=usuario, now=datetime.now())

    if request.method == 'POST':
        db.session.delete(usuario)
        db.session.commit()
        flash('Dados excluidos com sucesso!')
        return redirect(url_for('usuarios.list'))

