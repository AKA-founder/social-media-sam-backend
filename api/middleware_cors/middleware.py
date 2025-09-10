"""
Compatibility middleware.

If 'django-cors-headers' is installed, delegate to its CorsMiddleware.
Otherwise, act as a no-op so the app can boot without import errors.
 from corsheaders.middleware import CorsMiddleware as _CorsMiddleware  # type: ignore

    class CorsMiddleware(_CorsMiddleware):  # delegate to real impl
        pass

except Exception:  # fallback: no-op
    class CorsMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response
        def __call__(self, request):
            return self.get_response(request)
