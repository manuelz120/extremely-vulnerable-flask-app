FROM python:3.10.8-slim-buster

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

COPY conf/nginx.conf /etc/nginx
COPY --chown=www-data:www-data . /srv/flask_app

WORKDIR /srv/flask_app
RUN pip install -r requirements.txt --src /usr/local/src
CMD ["/bin/bash", "-e", "./start.sh"]