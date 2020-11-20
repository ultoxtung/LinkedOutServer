FROM python:3.8

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]

COPY ./backend /app/backend
COPY ./app /app/app
COPY ./manage.py /app/manage.py
COPY ./docker-entrypoint.sh .

CMD ["/bin/bash", "docker-entrypoint.sh"]
