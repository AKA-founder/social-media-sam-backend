# api/views/pmp_webhooks.py
import os, json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def pmpro_webhook(request):
    # GET -> hurtigt ping
    if request.method != "POST":
        return JsonResponse({"status": "ok", "method": request.method})

    # Tjek delt token
    expected = os.getenv("WEBHOOK_TOKEN", "")
    got = request.headers.get("X-AKA-Token", "")
    if not expected or got != expected:
        return HttpResponseForbidden("bad token")

    # Læs payload
    try:
        payload = json.loads(request.body or "{}")
    except Exception:
        payload = {}

    # TODO: behandl payload (gem ordre/medlemskab osv.)
    return JsonResponse({"status": "ok", "received": payload})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def pmp_webhook(request):
    if request.method != "POST":
        return JsonResponse({"status": "ok", "method": request.method}, status=200)
    try:
        body = request.body.decode("utf-8") or "{}"
        data = json.loads(body)
    except Exception:
        data = {}
    logger.info("pmp_webhook payload=%s", data)
    return JsonResponse({"status": "ok"})
