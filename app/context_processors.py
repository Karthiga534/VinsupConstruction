
from django.conf import settings

def my_env_var(request):
    return {
        'my_env_var': settings.JS_ENV
    }

