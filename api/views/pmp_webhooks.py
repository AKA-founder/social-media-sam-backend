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
