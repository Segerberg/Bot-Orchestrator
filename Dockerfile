FROM python:3.8-alpine

RUN adduser -D cin

WORKDIR /home/cin

COPY requirements.txt requirements.txt

RUN apk update

RUN apk add --no-cache --update \
  python3 \
  python3-dev \
  py3-gevent \
  uwsgi \
  uwsgi-python3 \
  uwsgi-http \
  uwsgi-gevent3 \
  make \
  libffi-dev \
  gcc \
  g++ \
  musl-dev \
  make \
  nano

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY files files
COPY main.py config.py boot.sh create_user.py bot_names.csv install_default_bots.py ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

RUN chown -R cin:cin ./
USER cin

# RUN flask db init
# RUN flask db migrate
# RUN flask db upgrade
#RUN python create_superuser.py
VOLUME /home/cin
EXPOSE 8080
ENTRYPOINT ["sh","boot.sh"]