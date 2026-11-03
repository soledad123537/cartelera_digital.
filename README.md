# Cartelera Digital (Tablón de Anuncios con Flask) — Actividad N° 4 (TEM-742)

Aplicación web para gestionar un tablón de anuncios con **Flask**, **Flask-SQLAlchemy**,
**Flask-Login** y **Bootstrap 5**. Usa el patrón **Application Factory** (`create_app()`)
y **Blueprints** modulares.

## Estructura

```
cartelera_digital/
├── run.py                 # punto de entrada
├── config.py              # configuración (BD, SECRET_KEY)
├── requirements.txt
├── schema.sql             # script SQL opcional para MySQL (bd_anuncios)
└── app/
    ├── __init__.py        # create_app() + registro de Blueprints
    ├── static/css/estilo.css  # estilos propios (paleta y contraste)
    ├── extensions.py      # db, login_manager
    ├── models.py          # Usuario, Categoria, Anuncio
    ├── main/              # página principal
    ├── auth/              # login / logout
    ├── usuarios/          # CRUD de usuarios
    ├── categorias/        # CRUD de categorías
    ├── anuncios/          # CRUD de anuncios
    └── templates/         # base.html + plantillas por módulo
```

## Base de datos `bd_anuncios`

| Tabla       | Campos principales                                                        |
|-------------|---------------------------------------------------------------------------|
| usuarios    | **id (PK)**, nombre, email (único), password_hash                         |
| categorias  | **id (PK)**, nombre (único), descripcion                                  |
| anuncios    | **id (PK)**, titulo, contenido, fecha, *usuario_id (FK)*, *categoria_id (FK)* |

Relaciones: un usuario tiene muchos anuncios (1:N) y una categoría tiene muchos anuncios (1:N).

## Instalación (Windows / VS Code)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Abre http://127.0.0.1:5000

**Usuario inicial:** `admin@admin.com` / `admin123`

## Base de datos: SQLite o MySQL

- **SQLite (por defecto):** no necesitas instalar nada; se crea el archivo `bd_anuncios.db`.
- **MySQL (XAMPP / phpMyAdmin):**
  1. Ejecuta `schema.sql` (crea la base `bd_anuncios` y las tablas).
  2. Antes de iniciar, define la variable de entorno:
     ```powershell
     $env:DATABASE_URL = "mysql+pymysql://root:@localhost/bd_anuncios"
     python run.py
     ```

## Subir a GitHub

```powershell
git init
git add .
git commit -m "Actividad 4: Cartelera Digital con Flask"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/cartelera_digital.git
git push -u origin main
```
