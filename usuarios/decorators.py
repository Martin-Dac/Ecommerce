from django.shortcuts import redirect
from django.contrib import messages
from .models import Usuario, Orden 

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwaargs):
        if request.user.is_authenticated:
            messages.error(request, "No se puede entrar porque ya iniciaste sesion")
            return redirect('home')
        else:
            return view_func(request, *args, **kwaargs)
    
    return wrapper_func

def Carrito_check(view_func):
    def function(request, *args, **kwaargs):
        user = request.user
        cliente = Usuario.objects.get(user = user)
        orden = Orden.objects.get(cliente=cliente, completado=False)
        Ordenitems = orden.ordenitem_set.all()
        if Ordenitems.exists():
            return view_func(request, *args, **kwaargs)
        else:
            messages.error(request, "No se puede comprar porque no hay productos")
            return redirect('home')
    
    return function
