from flask import session, redirect, url_for, render_template, request
from app import db, lm
from ..models import Category, Priority, Todo, User
from ..forms import NewTask
from . import main
from flask_login import current_user, login_required


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('auth.login'))

    access_token = access_token[0]

    return render_template('index.html',
                           categories=Category.query.all(),
                           todos=Todo.query.join(Priority).order_by(Priority.value.desc()))


@main.route('/new', methods=['GET', 'POST'])
def new():
    form = NewTask()
    if form.validate_on_submit() and request.method == 'POST':
        category = Category.query.filter_by(id=request.form['category']).first()
        priority = Priority.query.filter_by(id=request.form['priority']).first()
        todo = Todo(category, priority, description=form.description.data,
                    user=current_user._get_current_object())
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        return render_template('new.html', form=form, categories=Category.query.all(), priorities=Priority.query.all())
