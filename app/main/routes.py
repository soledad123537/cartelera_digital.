from flask import Blueprint, render_template, request

from app.models import Anuncio, Categoria

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def inicio():
    """Página principal: muestra los anuncios (filtrables por categoría)."""
    categoria_id = request.args.get('categoria', type=int)
    consulta = Anuncio.query.order_by(Anuncio.fecha.desc())
    if categoria_id:
        consulta = consulta.filter_by(categoria_id=categoria_id)
    anuncios = consulta.all()
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template('inicio.html', anuncios=anuncios,
                           categorias=categorias, categoria_id=categoria_id)
