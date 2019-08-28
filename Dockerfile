FROM python:3.7-slim

RUN apt-get update && apt-get install -y \
    netcat \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/audeeo

COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.python.org --disable-pip-version-check -r requirements.txt

COPY . /srv/audeeo

ENV FLASK_APP audeeo

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn-conf.py", "wsgi:app"]
