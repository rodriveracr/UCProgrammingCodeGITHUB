import os

class Config:
    # Clave secreta para la aplicación
    SECRET_KEY = 'your_secret_key'
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'  # Usa 'users.db' para tu base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Directorio donde se almacenarán los archivos subidos
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

    # Tamaño máximo permitido para archivos subidos (en bytes)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
