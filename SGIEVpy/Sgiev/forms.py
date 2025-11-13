from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuarios

class LoginForm(forms.Form):
    correo = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su correo',
            'required': 'required'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'required': 'required'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')
        password = cleaned_data.get('password')
        
        if correo and password:
            try:
                usuario = Usuarios.objects.get(correo=correo, activo=1)
                if not check_password(password, usuario.clave):
                    raise forms.ValidationError('Correo o contraseña incorrectos')
            except Usuarios.DoesNotExist:
                raise forms.ValidationError('Correo o contraseña incorrectos')
        
        return cleaned_data
