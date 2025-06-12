# Import the application factory and database instance from the ``__init__``
# module. Importing from ``app`` would cause this script to import itself and
# fail with a circular import error.
from __init__ import create_app, db

# Inicializar la aplicación
app = create_app()

# Crear el contexto de la aplicación para interactuar con la base de datos
with app.app_context():
    db.create_all()
    print("Base de datos creada exitosamente.")
