"""
CorsMiddleware compatibility shim.

- Hvis 'django-cors-headers' er installeret, delegér til dens CorsMiddleware.
- Ellers vær en no-op, så appen kan starte uden importfejl.
"""
try:
    from corsheaders.middleware import CorsMiddleware as _CorsMiddleware  # type: ignore

    class CorsMiddleware(_CorsMiddleware):
        pass

except Exception:
    class CorsMiddleware:
        def __init__(self, get_response): self.get_response = get_response
        def __call__(self, request): return self.get_response(request)
