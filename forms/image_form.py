from wtforms import Form, validators, URLField


class ImageForm(Form):
    url = URLField('url', [validators.DataRequired()])
