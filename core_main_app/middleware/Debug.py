import logging

logger = logging.getLogger(__name__)

class CsrfDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            csrf_cookie = request.COOKIES.get('csrftoken')
            csrf_token = request.POST.get('csrfmiddlewaretoken') or request.META.get('HTTP_X_CSRFTOKEN')
            logger.debug(f"CSRF Cookie: {csrf_cookie}")
            logger.debug(f"CSRF Token: {csrf_token}")
            if csrf_cookie and csrf_token:
                if csrf_cookie == csrf_token:
                    logger.debug("CSRF tokens match.")
                else:
                    logger.debug("CSRF tokens do not match.")
            else:
                logger.debug("Missing CSRF token or cookie.")
        response = self.get_response(request)
        return response
