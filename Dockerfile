FROM python:3.7-slim

# Use "RUN adduser -D -g '' newuser" for alpine
RUN adduser --disabled-password --gecos '' audeeo

WORKDIR /srv/audeeo

RUN apt-get update && apt-get install -y \
    netcat \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install \
    --trusted-host pypi.python.org \
    --disable-pip-version-check \
    -r requirements.txt

COPY audeeo audeeo
COPY migrations migrations
COPY gunicorn-conf.py wsgi.py docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

ENV FLASK_APP "audeeo"

USER audeeo

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
