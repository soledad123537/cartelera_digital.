from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Anuncio, Categoria

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios')


@anuncios_bp.route('/')
@login_required
def lista():
    anuncios = Anuncio.query.order_by(Anuncio.fecha.desc()).all()
    return render_template('anuncios/lista.html', anuncios=anuncios)


@anuncios_bp.route('/<int:id>')
def detalle(id):
    anuncio = db.get_or_404(Anuncio, id)
    return render_template('anuncios/detalle.html', anuncio=anuncio)


@anuncios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    categorias = Categoria.query.order_by(Categoria.nombre).all()

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        contenido = request.form.get('contenido', '').strip()
        categoria_id = request.form.get('categoria_id', type=int)

        if not titulo or not contenido or not categoria_id:
            flash('Título, contenido y categoría son obligatorios.', 'danger')
        else:
            anuncio = Anuncio(titulo=titulo, contenido=contenido,
                              categoria_id=categoria_id, usuario_id=current_user.id)
            db.session.add(anuncio)
            db.session.commit()
            flash('Anuncio publicado correctamente.', 'success')
            return redirect(url_for('anuncios.lista'))

    return render_template('anuncios/form.html', anuncio=None, categorias=categorias)


@anuncios_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    anuncio = db.get_or_404(Anuncio, id)
    categorias = Categoria.query.order_by(Categoria.nombre).all()

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        contenido = request.form.get('contenido', '').strip()
        categoria_id = request.form.get('categoria_id', type=int)

        if not titulo or not contenido or not categoria_id:
            flash('Título, contenido y categoría son obligatorios.', 'danger')
        else:
            anuncio.titulo = titulo
            anuncio.contenido = contenido
            anuncio.categoria_id = categoria_id
            db.session.commit()
            flash('Anuncio actualizado correctamente.', 'success')
            return redirect(url_for('anuncios.lista'))

    return render_template('anuncios/form.html', anuncio=anuncio, categorias=categorias)


@anuncios_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    anuncio = db.get_or_404(Anuncio, id)
    db.session.delete(anuncio)
    db.session.commit()
    flash('Anuncio eliminado.', 'success')
    return redirect(url_for('anuncios.lista'))
