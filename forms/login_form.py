from wtforms import Form, PasswordField, validators, EmailField


class LoginForm(Form):
    email = EmailField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
