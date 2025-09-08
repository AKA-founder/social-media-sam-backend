# path: Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl ca-certificates netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# App user
RUN useradd --create-home --shell /usr/sbin/nologin app
WORKDIR /app

# Dependencies first (cache)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install -r /app/requirements.txt

# App code
COPY . /app

# Prepare runtime dirs
RUN mkdir -p /app/staticfiles /app/mediafiles && chown -R app:app /app

# Entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER app
EXPOSE 8000
ENTRYPOINT ["entrypoint.sh"]

# 👉 Bind til Railway's $PORT (fallback til 8000 lokalt)
CMD ["sh","-c","gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3} --timeout 60"]
