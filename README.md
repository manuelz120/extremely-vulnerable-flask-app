# Extremely Vulnerable Flask App

[![Pylint](https://github.com/manuelz120/extremely-vulnerable-flask-app/actions/workflows/pylint.yml/badge.svg)](https://github.com/manuelz120/extremely-vulnerable-flask-app/actions/workflows/pylint.yml)

Intentionally vulnerable Python / Flask application, built for educational purposes.

## Setup

Using `python3` and [venv](https://docs.python.org/3/library/venv.html):

```bash
git clone git@github.com:manuelz120/extremely-vulnerable-flask-app.git
cd extremely-vulnerable-flask-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m flask run # Can be stopped using CTRL+C
```

Using `docker`:

```bash
git clone git@github.com:manuelz120/extremely-vulnerable-flask-app.git
cd extremely-vulnerable-flask-app
docker build . -t extremely_vulnerable_flask_app
docker run --name extremely_vulnerable_flask_app -p 5000:80 extremely_vulnerable_flask_app  # Can be stopped using CTRL+C or by running `docker kill extremely_vulnerable_flask_app`
```

Afterwards, the app should be running at http://localhost:5000
