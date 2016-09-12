from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, StringField, RadioField
from wtforms.validators import DataRequired, Regexp


class NewTask(Form):
    task = TextAreaField('Task')
    category = RadioField('Category', choices=[('1', 'Work'), ('2', 'Home')])
    priority = RadioField('Category', choices=[('3', 'high'), ('2', 'medium'), ('1', 'low')])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')
