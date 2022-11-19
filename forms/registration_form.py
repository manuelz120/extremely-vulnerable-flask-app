from wtforms import Form, StringField, PasswordField, validators, EmailField


class RegistrationForm(Form):
    email = EmailField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    registration_code = StringField('Registration Code',
                                    [validators.Length(min=5)])
