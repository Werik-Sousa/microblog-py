from flask import Blueprint, render_template, session
from app.database import db
from app.models import Usuario
from flask import request, redirect, flash, url_for
from app.decorators import login_required

bp_usuarios = Blueprint('usuarios', __name__)

@bp_usuarios.route('/')
@bp_usuarios.route('/index')
def index():
    return render_template('index.html')

def validar_usuario(nome, email, senha, csenha):
    if not nome or not email or not senha:
        return 'Preencha todos os campos'
    if senha != csenha:
        return 'As senhas não conferem'
    if Usuario.query.filter_by(email=email).first():
        return 'Email já cadastrado'
    return None

@bp_usuarios.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email, senha=senha).first()
        if not email or not senha:
            flash('Preencha todos os campos', 'warning')
            return redirect(url_for('usuarios.login'))
        if usuario:
            session['usuario_id'] = usuario.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('usuarios.list'))
        else:
            flash('Usuário não encontrado. Por favor, cadastre-se.', 'warning')
            return redirect(url_for('usuarios.create'))

    return render_template('login.html')


@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'GET':
        return render_template('usuarios_create.html')

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')

        erro = validar_usuario(nome, email, senha, csenha)
        if erro:
            flash(erro)
            return render_template('usuarios_create.html', nome=nome, email=email)

    usuario = Usuario(nome, email, senha)
    db.session.add(usuario)
    db.session.commit()

    flash('Usuário criado com sucesso!', 'success')
    return redirect(url_for('usuarios.login')) 

#list    
@bp_usuarios.route('/list')
@login_required
def list():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para ver a lista de usuários.', 'warning')
        return redirect(url_for('usuarios.login'))

    usuarios = Usuario.query.all()
    return render_template('usuarios_list.html', usuarios=usuarios)

#update  
@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('usuarios_update.html', usuario=usuario)

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')

        if not nome or not email:
            flash('Preencha todos os campos', 'warning')
            return redirect(url_for('usuarios.update', id=id))

        usuario.nome = nome
        usuario.email = email
        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('usuarios.list'))

#delete
@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('usuarios_delete.html', usuario=usuario)

    if request.method == 'POST':
        db.session.delete(usuario)
        db.session.commit()
        flash('Dados excluidos com sucesso!', 'success')
        return redirect(url_for('usuarios.list'))

@bp_usuarios.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'warning')
    return redirect(url_for('usuarios.login'))
