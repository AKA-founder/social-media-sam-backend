#!/bin/bash
set -euo pipefail

# — Info logs (WHY: se hvad containeren gør)
echo "[entrypoint] DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-<unset>}"
echo "[entrypoint] PORT=${PORT:-8000}  WORKERS=${GUNICORN_WORKERS:-3}"

# Optional JS replacements hvis filer findes og envs er sat
CHAT_JS_FILE="/app/web/static/chat.js"
SEARCH_JS_FILE="/app/web/static/search.js"

if [[ -f "$CHAT_JS_FILE" ]]; then
  [[ -n "${APP_URL:-}" ]] && sed -i "s|http://0.0.0.0:8000|${APP_URL}|g" "$CHAT_JS_FILE"
  [[ -n "${LNG_BOT:-}" ]]   && sed -i "s|Bot is Thinking...|${LNG_BOT}|g" "$CHAT_JS_FILE"
  [[ -n "${LNG_ERROR:-}" ]] && sed -i "s|error sending the message.|${LNG_ERROR}|g" "$CHAT_JS_FILE"
  [[ -n "${LNG_ASK:-}" ]]   && sed -i "s|Ask a question...|${LNG_ASK}|g" "$CHAT_JS_FILE"
  [[ -n "${LNG_WRITE:-}" ]] && sed -i "s|Write a reply...|${LNG_WRITE}|g" "$CHAT_JS_FILE"
fi

if [[ -f "$SEARCH_JS_FILE" && -n "${APP_URL:-}" ]]; then
  sed -i "s|http://0.0.0.0:8000|${APP_URL}|g" "$SEARCH_JS_FILE"
fi

echo "[entrypoint] Running migrate…"
python manage.py migrate --noinput
echo "[entrypoint] Running collectstatic…"
python manage.py collectstatic --noinput

echo "[entrypoint] Starting Gunicorn on 0.0.0.0:${PORT:-8000} …"
exec gunicorn dj_backend_server.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers ${GUNICORN_WORKERS:-3} \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
