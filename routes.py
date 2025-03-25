import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from .models import db, Archivo, User
from datetime import datetime

main = Blueprint('main', __name__)

# Carpeta de subida de archivos
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Función para verificar que el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rutas de las páginas estáticas
@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')

@main.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/encrypt')
@login_required
def encrypt():
    return render_template('encrypt.html')

@main.route('/decrypt')
@login_required
def decrypt():
    return render_template('decrypt.html')

# Ruta para la página de login
@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener el nombre de usuario y la contraseña del formulario
        username = request.form['username']
        password = request.form['password']

        # Buscar el usuario en la base de datos
        user = User.query.filter_by(username=username).first()

        # Validar si el usuario existe y si la contraseña es correcta
        if user and check_password_hash(user.password, password):
            login_user(user)  # Iniciar sesión
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('main.dashboard'))  # Redirigir al dashboard si el login es exitoso
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('main.login'))

    return render_template('index.html')

# Ruta para cerrar sesión
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('main.login'))

# Rutas para la gestión de archivos
@main.route('/dashboard')
@login_required
def dashboard():
    archivos = Archivo.query.filter_by(usuario_id=current_user.id).all()
    
    # Logic to check if a file is selected for preview
    selected_file_id = request.args.get('file_id')
    selected_file = None
    if selected_file_id:
        selected_file = Archivo.query.get(selected_file_id)
    
    return render_template('dashboard.html', archivos=archivos, selected_file=selected_file)

@main.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('main.dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('main.dashboard'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Guardar el archivo en la base de datos
        nuevo_archivo = Archivo(nombre=filename, ruta=file_path, fecha_subida=datetime.utcnow(), usuario_id=current_user.id)
        db.session.add(nuevo_archivo)
        db.session.commit()

        flash('Archivo subido exitosamente', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Tipo de archivo no permitido', 'danger')
    return redirect(url_for('main.dashboard'))

@main.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    archivo = Archivo.query.get(file_id)
    if archivo and archivo.usuario_id == current_user.id:
        return send_from_directory(UPLOAD_FOLDER, archivo.nombre, as_attachment=True)
    else:
        flash("No tienes permisos para descargar este archivo", 'danger')
        return redirect(url_for('main.dashboard'))

# Route to preview files
@main.route('/preview/<int:file_id>')
@login_required
def preview_file(file_id):
    archivo = Archivo.query.get(file_id)
    if archivo and archivo.usuario_id == current_user.id:
        return send_from_directory(UPLOAD_FOLDER, archivo.nombre)
    else:
        flash("No tienes permisos para ver este archivo", 'danger')
        return redirect(url_for('main.dashboard'))
