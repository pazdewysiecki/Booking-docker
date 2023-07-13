from python:3.12.0b3-alpine3.18
FROM python:3.12.0b3
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev
RUN pip3 install mysqlclient
RUN pip3 install django-simple-history


COPY requirements.txt /app/requirements.txt

RUN set -ex \
    &&  pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ADD . . 

#EXPOSE 8000

#CMD ["gunicorn", "--bind",  ":8000", "--workers", "3", "reservations.wsgi:application"]

CMD gunicorn reservations.wsgi:application --bind 0.0.0.0:$PORT 