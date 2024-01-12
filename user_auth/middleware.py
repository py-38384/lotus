from django.shortcuts import render, HttpResponse, redirect, HttpResponsePermanentRedirect
from .models import *
import re
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        return response
    def process_view(self, request, view_func, *args, **kwargs):
        if request.user.is_authenticated:
            email_verify_obj_exists = Email_Verified.objects.filter(user=request.user).exists()
            if email_verify_obj_exists:
                email_verify_obj = Email_Verified.objects.get(user=request.user)
                path = request.path_info.lstrip('/')
                is_admin_request = re.findall("^admin", path)
                is_static_request = re.findall("^static", path)
                if email_verify_obj.blocked:
                    if path == "user/block/":
                        return None
                    return redirect("block")
                if not email_verify_obj.email_verified:
                    if path == "user/conform_email/" or path == "user/change_email/" or path=="user/email_resend/" or is_admin_request or is_static_request:
                        return None
                    return redirect("conform_email")