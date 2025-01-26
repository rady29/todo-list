# Importando funcionalidades de la app
from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from todor import db

# Creando instancia
bp = Blueprint('auth', __name__, url_prefix='/auth')

#Creado ruta y función
@bp.route('/register', methods = ('GET', 'POST'))
def register():
    #Validación de datos
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Encriptando password
        user = User(username, generate_password_hash(password))

        # Manejo de errores
        error = None

        # Consultado a la base de datos
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f"El usuario {username} ya se encuentra registrado en la herramienta"
        flash(error)

    return render_template('auth/register.html')

# Manejo de Inicio de Sesión
@bp.route('/login', methods = ('GET', 'POST'))
def login():
    #Validación de datos
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Manejo de errores
        error = None

        # Consultado a la base de datos
        user = User.query.filter_by(username = username).first()
        if user == None:
            error = "Nombre de usuario incorrecto"
        elif not check_password_hash(user.password, password):
            error = "Contraseña incorrecta"

        # Iniciar sesión
        if error == None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('opciones.index'))

        flash(error)

    return render_template('auth/login.html')

# Manteniendo la sesión
@bp.before_app_request
def load_loggged_in_user():
    user_id = session.get('user_id')

    # Comparando
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

# Cerrando Sesión
@bp.route('/logout')
def logout():
        session.clear()
        return redirect(url_for('index'))

# Agregando verificación de inicio de  sesión
import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view