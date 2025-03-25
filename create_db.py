from app import create_app, db

# Inicializar la aplicación
app = create_app()

# Crear el contexto de la aplicación para interactuar con la base de datos
with app.app_context():
    db.create_all()
    print("Base de datos creada exitosamente.")
