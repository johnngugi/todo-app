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
        description = request.form['description']
        todo.category = category
        todo.priority = priority
        todo.description = description
        db.session.commit()
        return redirect('/')


# @main.route('/edit<int:id>')
# def edit(id):
#     if not current_user.social_id:
#         abort(403)
#
#     form = NewTask()
#     if request.method == 'POST':
#
#         task.category = form.category.data
#         task.priority = form.priority.data
#         db.session.commit()
#         return redirect(url_for('main.index', id=id))
#     return render_template('edit.html', form=form)

@main.route('/done')
def done():
    task = Todo.query.filter_by()


@main.route('/category')
@login_required
def category():
    return render_template('category.html')
