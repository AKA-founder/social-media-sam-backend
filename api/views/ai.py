import os
import time
from django.http import JsonResponse

try:
    import httpx  # bedre timeouts/retries end requests
except Exception:
    httpx = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ai_ping(_request):
    """
    Safe ping: kalder OpenAI GET /v1/models?limit=1 med korte timeouts.
    Lækker ikke secrets. Returnerer status + roundtrip + evt. HTTP-status eller fejldetaljer.
    """
    if not OPENAI_API_KEY:
        return JsonResponse({"status": "error", "error": "OPENAI_API_KEY missing"}, status=503)

    url = "https://api.openai.com/v1/models?limit=1"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Accept": "application/json",
    }

    started = time.perf_counter()
    try:
        if httpx is None:
            # Minimal fallback til stdlib
            import urllib.request
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                code = resp.getcode()
        else:
            with httpx.Client(timeout=httpx.Timeout(connect=2.0, read=3.0, write=3.0, pool=2.0)) as client:
                r = client.get(url, headers=headers)
                code = r.status_code

        ms = int((time.perf_counter() - started) * 1000)
        if 200 <= code < 300:
            return JsonResponse({"status": "ok", "openai_http_status": code, "roundtrip_ms": ms})
        # Non-2xx fra OpenAI = "degraded" (key forkert, plan, etc.)
        return JsonResponse({"status": "degraded", "openai_http_status": code, "roundtrip_ms": ms}, status=502)

    except Exception as exc:
        ms = int((time.perf_counter() - started) * 1000)
        # Returnér både type og besked for bedre triage
        return JsonResponse(
            {"status": "error", "error": type(exc).__name__, "detail": str(exc), "roundtrip_ms": ms},
            status=502,
        )
