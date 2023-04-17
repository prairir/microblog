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

# copy `migration` into the container as `migration`
COPY migrations migrations

# copy a bunch of stuff into the current directory in the container
COPY microblog.py config.py boot.sh ./

# make `boot.sh` executable
RUN chmod a+x boot.sh

# set environment variable `FLASK_APP` to `microblog.py`
ENV FLASK_APP microblog.py

# upgrade db
CMD flask db upgrade

# migrate db
CMD flask db migrate -m "two-factor authentication"

# upgrade db
CMD flask db upgrade

# make this directory owned by user `microblog`
RUN chown -R microblog:microblog ./

# set user to `microblog`
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
