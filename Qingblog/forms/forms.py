from flask.ext.wtf import Form
from wtforms.fields import TextAreaField, TextField, PasswordField
from wtforms.validators import Required

__all__ = [
    'LoginForm',
    'CommentForm',
    'SearchForm']


class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])


class CommentForm(Form):
    username = TextField('username', validators=[Required()], id='name')
    email = TextField('email', validators=[Required()], id='email')
    site = TextField('site', id='site')
    content = TextAreaField('content', validators=[Required()], id='content')


class SearchForm(Form):
    search = TextField('search', validators=[Required()])
