import os
def healthz(_request):
    return JsonResponse({'status': 'ok'})

"""
URL configuration for dj_backend_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from web.views.view_root import root_navigation_view


def readyz(_request):
    data = {"db": "unknown", "redis": "skipped"}



urlpatterns = [
    path('', include('web.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include the API URLs from the 'api' app,
    path('healthz', healthz),
    path('readyz', readyz),]
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

    status = 200 if data["db"] == "ok" and (data["redis"] in ("ok","skipped")) else 503
    return JsonResponse({"status": "ok" if status==200 else "degraded", **data}, status=status)
