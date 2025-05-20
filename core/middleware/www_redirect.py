from django.http import HttpResponsePermanentRedirect

class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host == 'astrometrika.com':
            return HttpResponsePermanentRedirect(
                request.build_absolute_uri().replace('://astrometrika.com', '://www.astrometrika.com')
            )
        return self.get_response(request)