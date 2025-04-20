from flask import Blueprint, render_template

bp_usuarios = Blueprint('usuarios', __name__)

@bp_usuarios.route('/create')
def create():
    return render_template('usuarios_create.html')