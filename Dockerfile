FROM python:3.7-slim

# Use "RUN adduser -D -g '' newuser" for alpine
RUN adduser --disabled-password --gecos '' audeeo

WORKDIR /srv/audeeo

RUN apt-get update && apt-get install -y \
    netcat \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/srv/audeeo/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install \
    --trusted-host pypi.python.org \
    --disable-pip-version-check \
    -r requirements.txt

COPY audeeo audeeo
COPY migrations migrations
COPY gunicorn-conf.py wsgi.py ./

ENV FLASK_APP "audeeo"

USER audeeo

EXPOSE 8000
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
