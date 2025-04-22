from flask import Blueprint, render_template
from app.database import db
from app.models import Usuario
from datetime import datetime

from flask import request, redirect, flash, url_for

bp_usuarios = Blueprint('usuarios', __name__)

@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'GET':
        return render_template('usuarios_create.html', now=datetime.now())

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')

        usuario = Usuario(nome, email, senha)
        db.session.add(usuario)
        db.session.commit()
        if not nome or not email or not senha:
            flash('Preencha todos os campos')
            return redirect('/usuarios/create')
        if senha != csenha:
            flash('As senhas não conferem')
            return redirect('/usuarios/create')
        return 'Usuário criado com sucesso!'
    
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
        return render_template('usuarios_update.html', usuario=usuario, now=datetime.now())

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')

        if not nome or not email or not senha:
            flash('Preencha todos os campos')
            return redirect(url_for('usuarios.update', id=id))
        if senha != csenha:
            flash('As senhas não conferem')
            return redirect(url_for('usuarios.update', id=id))

        usuario.nome = nome
        usuario.email = email
        usuario.senha = senha
        db.session.commit()
        return 'Usuário atualizado com sucesso!'

#delete
@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('usuarios_delete.html', usuario=usuario, now=datetime.now())

    if request.method == 'POST':
        db.session.delete(usuario)
        db.session.commit()
        return 'Usuário deletado com sucesso!'

