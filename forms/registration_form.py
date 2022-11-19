from wtforms import Form, BooleanField, StringField, PasswordField, validators, EmailField


class RegistrationForm(Form):
    email = EmailField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    registration_code = StringField('Registration Code',
                                    [validators.Length(min=32, max=32)])
