from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('/')
@login_required
def lista():
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template('usuarios/lista.html', usuarios=usuarios)


@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not nombre or not email or len(password) < 4:
            flash('Completa todos los campos (contraseña mínimo 4 caracteres).', 'danger')
        elif Usuario.query.filter_by(email=email).first():
            flash('Ya existe un usuario con ese correo.', 'danger')
        else:
            usuario = Usuario(nombre=nombre, email=email)
            usuario.set_password(password)
            db.session.add(usuario)
            db.session.commit()
            flash('Usuario registrado correctamente.', 'success')
            return redirect(url_for('usuarios.lista'))

    return render_template('usuarios/form.html', usuario=None)


@usuarios_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    usuario = db.get_or_404(Usuario, id)

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        repetido = Usuario.query.filter(Usuario.email == email, Usuario.id != id).first()
        if not nombre or not email:
            flash('Nombre y correo son obligatorios.', 'danger')
        elif repetido:
            flash('Ese correo ya pertenece a otro usuario.', 'danger')
        else:
            usuario.nombre = nombre
            usuario.email = email
            if password:  # solo se cambia si se escribió una nueva
                usuario.set_password(password)
            db.session.commit()
            flash('Usuario actualizado correctamente.', 'success')
            return redirect(url_for('usuarios.lista'))

    return render_template('usuarios/form.html', usuario=usuario)


@usuarios_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    usuario = db.get_or_404(Usuario, id)

    if usuario.id == current_user.id:
        flash('No puedes eliminar tu propio usuario.', 'danger')
    elif usuario.anuncios:
        flash('No se puede eliminar: el usuario tiene anuncios asociados.', 'danger')
    else:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado.', 'success')

    return redirect(url_for('usuarios.lista'))
