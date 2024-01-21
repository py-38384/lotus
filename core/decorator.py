from django.http import HttpResponse, Http404
from django.shortcuts import redirect
def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = None
            if request.user.is_authenticated and request.user.groups.exists():
                groups = request.user.groups.all()
                for group in groups:
                    if group.name in allowed_roles:
                        return view_func(request, *args, **kwargs)
            raise Http404()
        return wrapper_func
    return decorator