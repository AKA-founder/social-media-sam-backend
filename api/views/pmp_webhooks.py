import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from api.models import Membership

User = get_user_model()
SHARED_SECRET = os.getenv("PMP_WEBHOOK_SECRET", "")

def _json_error(msg, code=400):
    return JsonResponse({"status": "error", "error": msg}, status=code)

@csrf_exempt
def pmp_webhook(request):
    # Simpelt: forvent POST med form- eller JSON-data
    if request.method != "POST":
        return _json_error("POST required", 405)

    secret = request.headers.get("X-PMP-Secret") or request.POST.get("secret") or (request.GET.get("secret") if request.GET else "")
    if not SHARED_SECRET or secret != SHARED_SECRET:
        return _json_error("unauthorized", 401)
data = request.POST.dict() if request.POST else {}
    if not data:
        try:
            import json
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            data = {}

    email = (data.get("email") or "").strip().lower()
    active = str(data.get("active", "")).lower() in ("1","true","yes","active")
    level  = (str(data.get("level") or "")).strip()

    if not email:
        return _json_error("missing email")
 mem, _ = Membership.objects.get_or_create(email=email)
    mem.active = active
    mem.level = level
    # Link til eksisterende user hvis samme email findes
    if not mem.user_id:
        user = User.objects.filter(email__iexact=email).first()
        if user:
            mem.user = user
    mem.save()

    return JsonResponse({"status": "ok", "email": email, "active": mem.active, "level": mem.level, "updated_at": now()})
