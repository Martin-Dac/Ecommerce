from django.shortcuts import redirect
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwaargs):
        if request.user.is_authenticated:
            messages.error(request, "No se puede entrar porque ya iniciaste sesion")
            return redirect('home')
        else:
            return view_func(request, *args, **kwaargs)
    
    return wrapper_func