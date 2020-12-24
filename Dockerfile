FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./src/requirements.txt /var/www/requirements.txt

RUN pip install -r /var/www/requirements.txt

COPY ./src/ /app
