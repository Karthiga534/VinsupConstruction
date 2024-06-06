from django.http import HttpResponseRedirect
from django.urls import reverse

from django.http import HttpResponseRedirect
from django.urls import reverse

class RedirectUnauthorizedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.user)
        if not request.user.is_authenticated:

            return HttpResponseRedirect(reverse('unauthorized_page'))
        # return request
        response = self.get_response(request)
        return response

    def process_request(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('unauthorized_page'))
        return None




# api_key_auth.py

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse, NoReverseMatch

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.headers.get('X-API-Key')
        return self.get_response(request)
        try:
            admin_url = reverse('admin:index')
        except NoReverseMatch:
            admin_url = None

        # Allow access to the admin panel without API key
        if admin_url and request.path.startswith(admin_url):
            return self.get_response(request)
        
        # Allow access to media files without API key
        if request.path.startswith(settings.MEDIA_URL):
            api_key_param = request.GET.get('api_key')
            if api_key_param:
                api_key = api_key_param  
            
            response = self.get_response(request)
            response['Access-Control-Allow-Origin'] = '*' 
            response['Access-Control-Allow-Methods'] = 'GET'
            response['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type'
            return response
        
        # Apply API key validation only for API paths (e.g., /api/)
        if request.path.startswith('/add-uom/'):
            if api_key != settings.EXTERNAL_API_KEY:
                return JsonResponse({'error': ['Unauthorized']}, status=401)

        # For all other paths, allow the request to pass through
        return self.get_response(request)
