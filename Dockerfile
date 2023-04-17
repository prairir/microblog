# base docker container
FROM python:slim

# create user microblog
RUN useradd microblog

# make the default and work directory `/home/microblog`
WORKDIR /home/microblog

# copy `requirements.txt`
COPY requirements.txt requirements.txt

# make a venv
RUN python -m venv venv

# install `requirements.txt` in venv
RUN venv/bin/pip install -r requirements.txt

# install a bunch of stuff in venv
RUN venv/bin/pip install gunicorn pymysql cryptography

# copy `.env` into the container as `.env`
COPY .env .env

# copy `app` into the container as `app`
COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP microblog.py

CMD flask db upgrade
CMD flask db migrate -m "two-factor authentication"
CMD flask db upgrade

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
