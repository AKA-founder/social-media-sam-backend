from django.http import JsonResponse

def status(_request):
    return JsonResponse({"status": "ok", "service": "backend"})

