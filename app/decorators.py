from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from .utils import get_user_company,get_company_id

def check_user_company(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user  # Assuming `user` is available in the request
        company, company_msg = get_user_company(user)
        if not company:
            return JsonResponse({"details": company_msg}, status=401)
        request.company = company
        request.company_id = get_company_id(company)
        return view_func(request, *args, **kwargs)
    return _wrapped_view



def check_valid_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user  
        if user.disable :
            return JsonResponse({"details": "you are not allowed"}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def check_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user  
        print(user.admin)
        if  not user.admin :
            return redirect('login')
            return JsonResponse({"details": "you are not allowed"}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


