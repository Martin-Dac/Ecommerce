from django.forms import CheckboxInput, ModelForm, EmailInput, TextInput, PasswordInput, CharField, NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Producto, Usuario, direccion_envio


class LoginForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username' : TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Nombre de usuario',
            }),
            'password' : PasswordInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Contraseña',
            }),
        }
        labels={
            'username' : 'Nombre de Usuario',
            'password' : 'Contraseña'
        }

class SingIn(UserCreationForm):
    
    password1 = CharField(
        label = "Contraseña",
        widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'Contraseña'
        })
    )

    password2 = CharField(
        label = "Confirmar contraseña",
        widget = PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Repita contraseña'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        widgets = {
            'email': EmailInput(attrs={
                'class' : 'form-control',
                'max_length' : '100',
                'placeholder' : 'MailDeEjemplo@gmail.com',
            }),
            'username' : TextInput(attrs={
                'class' : 'form-control',
                'max_length' : '100',
                'placeholder' : 'Nombre de Usuario',
            })
        }
        labels={
            'username' : 'Nombre de Usuario',
            'email' : 'Mail',
        }

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = ('name', 'precio', 'digital', 'imagen', 'stock')
        widgets = {
            'name': TextInput(attrs={
                'class' : 'form-control',
                'max_length' : '100',
            }),
            'precio' : NumberInput(attrs={
                'class' : 'form-control',
                'max_length' : '100',
            })
        }
        labels={
            'name' : 'Nombre del Producto',
            'digital' : 'Es digital?',
            'stock' : 'Cuanto stock tenes?'
        }

class ActuUsuario(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'vendedor' : CheckboxInput(attrs={
                'class' : 'form-control',
            })
        }
        labels={
            'name' : 'Nombre de usuario',
            'vendedor' : 'Quiere ser vendedor?',
        }
    
    field_order = ['name', 'email', 'vendedor']
