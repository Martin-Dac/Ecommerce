from django.forms import ModelForm, EmailInput, TextInput, PasswordInput, CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
                'placeholder' : 'Nombre de Usuario'
            })
        }
        labels={
            'username' : 'Nombre de Usuario',
            'email' : 'Mail',
        }