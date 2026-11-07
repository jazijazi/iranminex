import threading
from typing import Optional
from django.http import HttpRequest

_thread_locals = threading.local()


def get_current_request() -> Optional[HttpRequest]:
    """Retrieve the current HTTP request from thread-local storage."""
    return getattr(_thread_locals, 'request', None)


class CurrentRequestMiddleware:
    """
    Stores the current request in thread-local storage so it can be
    accessed anywhere in the request cycle (e.g. model save()).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ⬆️ BEFORE the view
        _thread_locals.request = request        # runs BEFORE view
        
        # ────────────────────────────────────
        response = self.get_response(request)   # 👈 VIEW RUNS HERE
        # ────────────────────────────────────
        
        # ⬇️ AFTER the view
        _thread_locals.__dict__.pop('request', None)   # runs AFTER view
        
        return response