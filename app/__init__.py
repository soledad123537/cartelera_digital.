from flask import Flask

from config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    """Application Factory: crea y configura la aplicación."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # Registro de Blueprints
    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.usuarios.routes import usuarios_bp
    from app.categorias.routes import categorias_bp
    from app.anuncios.routes import anuncios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(anuncios_bp)

    with app.app_context():
        db.create_all()
        _datos_iniciales()

    return app


def _datos_iniciales():
    """Crea un usuario administrador y categorías por defecto si la BD está vacía."""
    from app.models import Usuario, Categoria

    if Usuario.query.count() == 0:
        admin = Usuario(nombre='Administrador', email='admin@admin.com')
        admin.set_password('admin123')
        db.session.add(admin)

    if Categoria.query.count() == 0:
        db.session.add_all([
            Categoria(nombre='General', descripcion='Avisos generales'),
            Categoria(nombre='Eventos', descripcion='Actividades y eventos'),
            Categoria(nombre='Académico', descripcion='Información académica'),
        ])

    db.session.commit()
