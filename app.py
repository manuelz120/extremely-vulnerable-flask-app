#!/usr/bin/env python3

from flask_bootstrap import Bootstrap5
from flask import Flask, render_template
from routes import init

app = Flask(__name__)
app.secret_key = 'super secret key'
bootstrap = Bootstrap5(app)

init()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/hello/')
def hello():
    return render_template('base.html')
