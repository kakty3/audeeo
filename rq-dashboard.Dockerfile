FROM python:3.7.0-alpine

RUN pip install rq-dashboard

EXPOSE 9181

CMD ["rq-dashboard"]
