FROM python:3.10.8-slim-buster

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential \
    && apt-get -y install uwsgi \
    && apt-get -y install uwsgi-plugin-python3

COPY conf/nginx.conf /etc/nginx
COPY --chown=www-data:www-data . /srv/flask_app

WORKDIR /srv/flask_app
RUN pip install -r requirements.txt --src /usr/local/src
CMD service nginx start; uwsgi --ini uwsgi.ini