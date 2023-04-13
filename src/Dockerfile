# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
ENV PYTHONPATH=/code
ENV FLASK_APP=/code/src/__init__.py
RUN apt-get update && apt-get install -y python3-dev supervisor nginx \
    && rm -rf /var/lib/apt/lists/*
COPY . /code/src/
RUN pip install -r src/requirements.txt
COPY uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY supervisord.ini /etc/supervisor/conf.d/supervisord.ini
COPY entrypoint.sh /entrypoint.sh
ENV RUNNING_ON_DOCKER_RUNNING Yes
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.ini"]
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "$INST"]