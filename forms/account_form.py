from wtforms import Form, PasswordField, EmailField, BooleanField


class AccountForm(Form):
    email = EmailField('Email Address')
    password = PasswordField('Password')
    password_control = PasswordField('Password Control')
    is_admin = BooleanField('Is Admin')
