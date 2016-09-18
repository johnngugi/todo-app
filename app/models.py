from datetime import datetime
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)

    def __init__(self, social_id, nickname):
        self.social_id = social_id
        self.nickname = nickname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_confirmed(self):
        return True

    def is_anonymous(self):
        return False


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    priority_id = db.Column('priority_id', db.Integer, db.ForeignKey('priority.id'))
    description = db.Column('description', db.String(255))
    creation_date = db.Column('creation_date', db.Date)
    is_done = db.Column('is_done', db.Boolean)

    category = db.relationship('Category', foreign_keys=category_id, backref="todos")
    priority = db.relationship('Priority', foreign_keys=priority_id, backref="todos")
    user = db.relationship('User', foreign_keys=user_id, backref="author")

    def __init__(self, category, priority, description, user):
        self.category = category
        self.priority = priority
        self.user = user
        self.description = description
        self.creation_date = datetime.utcnow()
        self.is_done = False


class Priority(db.Model):
    __tablename__ = "priority"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    value = db.Column('value', db.Integer)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))

    def __init__(self, name):
        self.name = name
