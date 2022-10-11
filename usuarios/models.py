from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Usuario(models.Model):
    name = models.CharField(max_length=100, null=True)
    vendedor = models.BooleanField(default=False, null=True)
    email = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=CASCADE, null=True)
    def __str__(self):
        return self.name

class Producto(models.Model):
    name = models.CharField(max_length=100, null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    digital = models.BooleanField(default=False, null=True)
    vendido_por = models.ForeignKey(Usuario, on_delete=CASCADE, null=True)
    imagen = models.ImageField(null=True, blank=True)
    stock = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    @property
    def ImagenURL(self):
        try:
            url = self.imagen.url
        except:
            url =''
        return url

class Orden(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True)
    Fecha_Orden = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False, null=True)
    ID_transaccion = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        ordenitems = self.ordenitem_set.all()
        for i in ordenitems:
            if i.producto.digital == False:
                shipping = True
        return shipping


    @property
    def Items_Carrito(self):
        ordenitems = self.ordenitem_set.all()
        total = sum([item.Cantidad for item in ordenitems])
        return total

    @property
    def Total_Carrito(self):
        ordenitems = self.ordenitem_set.all()
        total = 0
        for items in ordenitems:
            total2 = items.total_orden()
            total = total + total2 
        return total

class OrdenItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, blank=True, null=True)
    orden = models.ForeignKey(Orden, on_delete=models.SET_NULL, blank=True, null=True)
    Cantidad = models.IntegerField(default=0, null=True, blank=True)
    Fecha_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.producto.name

    def total_orden(self):
        total = self.Cantidad * self.producto.precio
        return total

class direccion_envio(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True)
    orden = models.ForeignKey(Orden, on_delete=models.SET_NULL, blank=True, null=True)
    direccion = models.CharField(max_length=100, null=True)
    ciudad = models.CharField(max_length=100, null=True)
    provincia = models.CharField(max_length=100, null=True)
    cod_postal = models.CharField(max_length=100, null=True)
    Fecha_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.direccion


#Cuando sea crea user tambien se crea la clase Usuario

@receiver(post_save, sender=User)
def crear_Usuario(sender, instance, created, **kwargs):

    if created:
        Usuario.objects.create(user = instance, name=instance.username, email=instance.email)
    

