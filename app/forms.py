from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Regexp


class NewTask(Form):
    task = TextAreaField('Task')
    category = SelectField('Category', choices=[('1', 'Work'), ('2', 'Home')])
    priority = SelectField('Priority', choices=[('3', 'high'), ('2', 'medium'), ('1', 'low')])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')
