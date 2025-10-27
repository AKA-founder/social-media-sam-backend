from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
import os

def healthz(_request):
    return JsonResponse({"status": "ok"})

def readyz(_request):
    data = {"db": "unknown", "redis": "skipped"}
    try:
        from django.db import connections
        conn = connections["default"]
        conn.ensure_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        data["db"] = "ok"
    except Exception as exc:
        data["db"] = f"error: {type(exc).__name__}"

    REDIS_URL = os.getenv("REDIS_URL") or os.getenv("REDISCLOUD_URL") or os.getenv("UPSTASH_REDIS_URL")
    if REDIS_URL:
        try:
            import redis  # type: ignore
            r = redis.from_url(REDIS_URL, socket_connect_timeout=1, socket_timeout=1)
            r.ping()
            data["redis"] = "ok"
        except Exception as exc:
            data["redis"] = f"error: {type(exc).__name__}"


    # OpenAI key status (ingen hemmeligheder lækkes)
    data["openai"] = "configured" if os.getenv("OPENAI_API_KEY") else "missing"

    status = 200 if data["db"] == "ok" and (data["redis"] in ("ok","skipped")) else 503
    return JsonResponse({"status": "ok" if status == 200 else "degraded", **data}, status=status)

urlpatterns = [
    path('', include('web.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('healthz', healthz),
    path('readyz', readyz),
]
