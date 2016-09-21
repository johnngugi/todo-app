from flask import session, redirect, url_for, render_template, request, g, flash
from app import db, lm
from ..models import Category, Priority, Todo, User
from . import main
from flask_login import current_user, login_required


@lm.user_loader
def load_user(social_id):
    current_user = User.query.get(social_id)
    return current_user


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
                           todos=Todo.query.join(User))


@main.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        category = Category.query.filter_by(id=request.form['category']).first()
        priority = Priority.query.filter_by(id=request.form['priority']).first()
        todo = Todo(category, priority, request.form['description'], user=current_user._get_current_object())
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    else:
        return render_template(
            'new.html',
            categories=Category.query.all(),
            priorities=Priority.query.all()
        )


@main.route('/update/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template(
            'edit.html',
            todo=todo,
            categories=Category.query.all(),
            priorities=Priority.query.all()
        )
    else:
        category = Category.query.filter_by(id=request.form['category']).first()
        priority = Priority.query.filter_by(id=request.form['priority']).first()
        description = request.form['description']
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


@main.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    return render_template('category.html', categories=Category.query.all())


@main.route('/new_category', methods=['GET', 'POST'])
@login_required
def new_category():
    if request.method == 'POST':
        name = request.form['category']
        new_category = Category(name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('main.category'))
    else:
        return render_template('newcat.html')


@main.route('/update_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def update_category(category_id):
    category = Category.query.get(category_id)
    if request.method == 'GET':
        return render_template('newcat.html')
    else:
        categoryname = request.form['category']
        category.name = categoryname
        db.session.commit()
        return redirect(url_for('main.category'))


@main.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if request.method == 'POST':
        category = Category.query.get(category_id)
        if not category.todos:
            db.session.delete(category)
            db.session.commit()
        else:
            flash("You have todos with that category")
        return redirect(url_for('main.category'))
