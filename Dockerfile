FROM python:3.7

WORKDIR /app

COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./app /app

EXPOSE 8000

 CMD ["python", "-m", "app"]
