# Importando Blueprint
from flask import Blueprint, render_template, request, redirect, url_for, g

# Agregando validación
from todor.auth import login_required
from .models import Todo, User
from todor import db

# Creando instancia
bp = Blueprint('todo', __name__, url_prefix='/opciones')

# Creado ruta y función
# Acción para listar tareas
@bp.route('/list')
@login_required
def index():
    todos = Todo.query.all()
    return render_template('opciones/index.html', todos = todos)

# Acción para crear listas
@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(g.user.id, title, desc)

        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('opciones.index'))
    return render_template('opciones/create.html')

def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo

# Acción para actualizar
@bp.route('/update/<int:id>', methods=('GET','POST'))
@login_required
def update(id):

    todo = get_todo(id)

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.state = True if request.form.get('state') == 'on' else False

        db.session.commit()
        return redirect(url_for('opciones.index'))
    return render_template('opciones/update.html', todo = todo)

# Acción para eliminar
@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('opciones.index'))