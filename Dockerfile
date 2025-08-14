# Use an official Python runtime as a parent image
FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=dj_backend_server.settings

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
