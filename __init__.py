from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuración de la clave secreta
    app.secret_key = 'supersecretkeythatshouldberandomandunique'

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración del correo electrónico
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'rovicr@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ftnx rehi gbvq yfbj'
    app.config['MAIL_DEFAULT_SENDER'] = 'rovicr@gmail.com'

    db.init_app(app)
    mail.init_app(app)

    # Inicializar LoginManager con la aplicación
    login_manager.init_app(app)
    login_manager.login_view = 'main.index'

    # Inicializar Flask-Migrate con la aplicación y la base de datos
    migrate.init_app(app, db)

    # Función para cargar el usuario
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar el Blueprint principal
    from .routes import main
    app.register_blueprint(main)

    # Registrar el Blueprint para los manejadores de errores
    from .error_handlers import error_bp
    app.register_blueprint(error_bp)

    return app
