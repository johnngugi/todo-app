from flask import session, redirect, url_for, render_template, request, g, abort
from app import db, lm
from ..models import Category, Priority, Todo, User
from ..forms import NewTask
from . import main
from flask_login import current_user, login_required


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.before_request
def before_request():
    g.user = current_user
    if not current_user.is_authenticated:
        return redirect(url_for('auth.authorize'))


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('auth.login'))

    access_token = access_token[0]

    return render_template('index.html',
                           categories=Category.query.all(),
                           todos=Todo.query.join(Priority).order_by(Priority.value.desc()))


@main.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = NewTask()
    if request.method == 'POST':
        category = Category.query.filter_by(id=form.category.data).first()
        priority = Priority.query.filter_by(id=form.priority.data).first()
        todo = Todo(category, priority, request.form['description'], user=current_user._get_current_object())
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    else:
        return render_template(
            'new.html',
            categories=Category.query.all(),
            priorities=Priority.query.all(),
            form=form)


@main.route('/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    form = NewTask()
    todo = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template(
            'edit.html',
            todo=todo,
            categories=Category.query.all(),
            priorities=Priority.query.all(),
            form=form
        )
    else:
        category = Category.query.filter_by(id=form.category.data).first()
        priority = Priority.query.filter_by(id=form.priority.data).first()
        description = form.description.data
        todo.category = category
        todo.priority = priority
        todo.description = description
        db.session.commit()
        return redirect('/')


@main.route('/delete-todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')


@main.route('/mark-done/<int:todo_id>', methods=['POST'])
def mark_done(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        todo.is_done = True
        db.session.commit()
        return redirect('/')


@main.route('/category')
@login_required
def category():
    if request.method == 'POST':
        category = Category(name=request.form['category'])
        db.session.add(category)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('category.html', categories=Category.query.all(),
                               todos=Todo.query.join(Priority).order_by(Priority.value.desc()))


# @main.route('/updatecat/<int:todo_id>', methods=['GET', 'POST'])
# def update_category():
#
