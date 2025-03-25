from flask_login import UserMixin
from . import db
from datetime import datetime

# Modelo de Usuario
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Relación: un usuario puede subir varios archivos
    archivos = db.relationship('Archivo', backref='usuario', lazy=True)

    # Implementación de los métodos requeridos por Flask-Login
    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


# Modelo de Archivo
class Archivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    ruta = db.Column(db.String(300), nullable=False)  # La ubicación del archivo en el servidor
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    encriptado = db.Column(db.Boolean, default=True)  # Indica si el archivo está encriptado
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Usuario que subió el archivo

    # Relación con la tabla de permisos
    permisos = db.relationship('Permiso', backref='archivo', lazy=True)


# Modelo de Permiso (Qué usuarios tienen acceso a qué archivos)
class Permiso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    archivo_id = db.Column(db.Integer, db.ForeignKey('archivo.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Usuario que tiene acceso

    # Relación de permisos con usuarios y archivos
    usuario = db.relationship('User', backref='permisos', lazy=True)
