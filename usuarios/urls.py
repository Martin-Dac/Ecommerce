import imp
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('productos/<int:id>', views.productos, name="productos"),
    path('clientes/', views.clientes, name="clientes"),
    path('carrito/', views.Carrito, name="carrito"),
    path('logout/', views.LogoutUser, name="logout"),
    path('login/', views.Login, name="login"),
    path('vender/', views.Vender, name="vender"),
    path('Buscar_Producto/', views.Buscar_Productos, name="Buscar_Productos"),

    path('update_Item/', views.updateItem, name="update_Item"),
    path('deleteProducto/<int:id>', views.deleteProducto, name="delete_producto")
]