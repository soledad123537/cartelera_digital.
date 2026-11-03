import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cambia-esta-clave-en-produccion')

    # Por defecto usa SQLite (archivo bd_anuncios.db), no requiere instalar nada.
    # Para usar MySQL define la variable de entorno DATABASE_URL, por ejemplo:
    #   mysql+pymysql://root:@localhost/bd_anuncios
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(BASE_DIR, 'bd_anuncios.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
