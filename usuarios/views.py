import imp
import json
from unicodedata import category
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime


from .models import Usuario, Producto, Orden, OrdenItem, direccion_envio
from .forms import LoginForm, SingIn, ProductoForm, ActuUsuario
from .decorators import unauthenticated_user

def Venta_check(user):
    if user.is_authenticated:
        a = Usuario.objects.get(user=user)
        return a.vendedor
    else:
        return False

# Create your views here.

def home(request):

    if request.user.is_authenticated:
        cliente = request.user.usuario
        orden, creada = Orden.objects.get_or_create(cliente=cliente, completado=False)
        cartItems = orden.Items_Carrito
    else:
        orden = {'Items_Carrito':0, 'Total_Carrito':0, 'shipping':False}
        cartItems = orden['Total_Carrito']

    productos = Producto.objects.all()
    context = {'productos':productos, 'cartItems': cartItems}
    return render(request, 'usuarios/home.html', context)

def productos(request, id=None):
    producto = Producto.objects.get(id = id)
    productos = Producto.objects.filter(name=producto.name)
    orden, creada = Orden.objects.get_or_create(cliente=request.user.usuario, completado=False)
    cartItems = orden.Items_Carrito
    context = {'productos': productos, 'cartItems': cartItems}
    return render(request, 'usuarios/productos.html', context)

@login_required(login_url='login')
def clientes(request):
    cliente = request.user.usuario
    form = ActuUsuario(instance=cliente)
    productos = Producto.objects.filter(vendido_por = cliente)
    orden, creada = Orden.objects.get_or_create(cliente=cliente, completado=False)
    cartItems = orden.Items_Carrito

    if request.method == 'POST':
        form = ActuUsuario(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')

    context ={'form': form, 'productos':productos, 'cartItems': cartItems}
    return render(request, 'usuarios/clientes.html', context)

@login_required(login_url='login')
def Carrito(request):
    if request.user.is_authenticated:
        cliente = request.user.usuario
        orden, creada = Orden.objects.get_or_create(cliente=cliente, completado=False)
        OrdenItems = orden.ordenitem_set.all()
        cartItems = orden.Items_Carrito
    else:
        OrdenItems = []
        orden = {'Items_Carrito':0, 'Total_Carrito':0, 'shipping':False}
        cartItems = orden['Total_Carrito']

    context = {'OrdenItems':OrdenItems, 'orden':orden, 'cartItems': cartItems}
    return render(request, 'usuarios/Carrito.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('home')

def updateItem(request):
    data = json.loads(request.body)
    productoId = data['productoId']
    accion = data['accion']

    print('Accion', accion)
    print('Producto', productoId)

    cliente = request.user.usuario
    producto = Producto.objects.get(id=productoId)
    orden, creada = Orden.objects.get_or_create(cliente=cliente, completado=False)
    ordenItem, creada = OrdenItem.objects.get_or_create(orden = orden, producto = producto)

    if accion == 'add':
        ordenItem.Cantidad = (ordenItem.Cantidad + 1)
    elif accion == 'remove':
        ordenItem.Cantidad = (ordenItem.Cantidad - 1)
    
    ordenItem.save()

    if ordenItem.Cantidad <= 0:
        ordenItem.delete()

    return JsonResponse('Item agregado', safe=False)

@unauthenticated_user
def Login(request):
    form = LoginForm
    formSingIn = SingIn

    if request.method == 'POST':
        if request.POST.get('submit') == 'Login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                form = LoginForm(request.POST)
                return redirect('home')

            else:
                messages.info(request, 'Nombre de usuario o contraseña incorrectos')

        elif request.POST.get('submit') == 'SingIn':
            formSingIn = SingIn(request.POST)
            if formSingIn.is_valid():
                Nuevo_user = formSingIn.save()
                Nuevo_user = authenticate(username = formSingIn.cleaned_data['username'], password = formSingIn.cleaned_data['password1'])
                login(request, Nuevo_user)
                return redirect('home')

    context = {'form': form, 'FormSingIn': formSingIn}
    return render(request, 'usuarios/Login.html', context)


@user_passes_test(Venta_check, login_url='home')
def Vender(request):
    form = ProductoForm
    orden, creada = Orden.objects.get_or_create(cliente=request.user.usuario, completado=False)
    cartItems = orden.Items_Carrito

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():
            Producto = form.save(commit=False)
            Producto.vendido_por = Usuario.objects.get(user = request.user)
            form.save()
            return redirect('home')

    context = {'form': form, 'cartItems': cartItems} 
    return render(request, 'usuarios/vender.html', context)

def Buscar_Productos(request):
    if request.method == 'POST':
        buscar = request.POST['search']
        productos = Producto.objects.filter(name__contains=buscar)
        context = {'Buscar': buscar, 'productos':productos}
        return render(request, 'usuarios/BuscarProductos.html', context)
    
    return render(request, 'usuarios/BuscarProductos.html')

def deleteProducto(request, id):
    producto = Producto.objects.get(id = id)
    producto.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='login')
def checkout(request):

    if request.user.is_authenticated:
        cliente = request.user.usuario
        orden, creada = Orden.objects.get_or_create(cliente=cliente, completado=False)
        OrdenItems = orden.ordenitem_set.all()
        cartItems = orden.Items_Carrito
    
    else:
        OrdenItems = []
        orden = {'Items_Carrito':0, 'Total_Carrito':0, 'shipping':False}
        cartItems = orden['Total_Carrito']

    context = {'OrdenItems':OrdenItems, 'orden':orden, 'cartItems': cartItems}
    return render(request, 'usuarios/Checkout.html', context)

def ProcesarOrden(request):
    data = json.loads(request.body)
    transaccion_ID = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        cliente = request.user.usuario
        orden, creada = Orden.objects.get_or_create(cliente=cliente, completado=False)
        total = float(data['form']['total'])
        orden.ID_transaccion = transaccion_ID

        if total == orden.Total_Carrito:
            orden.completado = True
        orden.save()

        if orden.shipping == True:
            direccion_envio.objects.create(
                cliente= cliente,
                orden= orden,
                direccion= data['shipping']['direccion'],
                ciudad= data['shipping']['ciudad'],
                provincia= data['shipping']['provincia'],
                cod_postal= data['shipping']['CodPostal'],
            )

    return JsonResponse('pago completo', safe=False)

