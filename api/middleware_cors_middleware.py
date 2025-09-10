"""
Shim so both 'api.middleware_cors_middleware.CorsMiddleware' and
'api.middleware_cors.middleware.CorsMiddleware' work.
"""
try:
    from api.middleware_cors.middleware import CorsMiddleware  # our real impl
except Exception:
    class CorsMiddleware:
        def __init__(self, get_response): self.get_response = get_response
        def __call__(self, request): return self.get_response(request)
