from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.extensions import db
from app.models import Categoria

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')


@categorias_bp.route('/')
@login_required
def lista():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template('categorias/lista.html', categorias=categorias)


@categorias_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
        elif Categoria.query.filter_by(nombre=nombre).first():
            flash('Ya existe una categoría con ese nombre.', 'danger')
        else:
            db.session.add(Categoria(nombre=nombre, descripcion=descripcion))
            db.session.commit()
            flash('Categoría registrada correctamente.', 'success')
            return redirect(url_for('categorias.lista'))

    return render_template('categorias/form.html', categoria=None)


@categorias_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    categoria = db.get_or_404(Categoria, id)

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        repetida = Categoria.query.filter(Categoria.nombre == nombre, Categoria.id != id).first()
        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
        elif repetida:
            flash('Ya existe otra categoría con ese nombre.', 'danger')
        else:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            db.session.commit()
            flash('Categoría actualizada correctamente.', 'success')
            return redirect(url_for('categorias.lista'))

    return render_template('categorias/form.html', categoria=categoria)


@categorias_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    categoria = db.get_or_404(Categoria, id)

    if categoria.anuncios:
        flash('No se puede eliminar: la categoría tiene anuncios asociados.', 'danger')
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada.', 'success')

    return redirect(url_for('categorias.lista'))
