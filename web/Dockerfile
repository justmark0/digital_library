FROM python:3.8.1-alpine

RUN apk --update add postgresql-dev gcc python3-dev musl-dev netcat-openbsd

RUN adduser -D library

WORKDIR /home/library

COPY requirements.txt requirements.txt
#RUN python3 -m venv venv
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install gunicorn

COPY app app
#COPY migrations migrations
COPY tests.py main.py config.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

RUN chown -R library:library ./

USER library

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
