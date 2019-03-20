FROM python:3.7

RUN apt-get update && apt-get install -y \
    netcat \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/audeeo

COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /srv/audeeo

EXPOSE 8000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
