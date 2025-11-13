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

class LoginForm(forms.Form):
    correo = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingrese su correo',
            'required': 'required'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
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


class UsuarioForm(forms.ModelForm):
    """
    Formulario para crear y editar usuarios
    """
    # Campo de contraseña personalizado
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la contraseña'
        }),
        required=False,
        help_text='Deje en blanco para mantener la contraseña actual (solo en edición)'
    )
    
    password_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme la contraseña'
        }),
        required=False
    )
    
    class Meta:
        model = Usuarios
        fields = [
            'num_identificacion',
            'tipo_usu',
            'p_nombre',
            's_nombre',
            'p_apellido',
            's_apellido',
            'correo',
            'telefono',
            'salario',
            'fecha_nacimiento',
            'direccion',
            'activo'
        ]
        
        widgets = {
            'num_identificacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de identificación'
            }),
            'tipo_usu': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('administrador', 'Administrador'),
                ('operario', 'Operario')
            ]),
            'p_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primer nombre'
            }),
            's_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Segundo nombre (opcional)'
            }),
            'p_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primer apellido'
            }),
            's_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Segundo apellido (opcional)'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '3001234567'
            }),
            'salario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Salario mensual'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa'
            }),
            'activo': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                (1, 'Activo'),
                (0, 'Inactivo')
            ])
        }
        
        labels = {
            'num_identificacion': 'Número de Identificación',
            'tipo_usu': 'Tipo de Usuario',
            'p_nombre': 'Primer Nombre',
            's_nombre': 'Segundo Nombre',
            'p_apellido': 'Primer Apellido',
            's_apellido': 'Segundo Apellido',
            'correo': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'salario': 'Salario',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Dirección',
            'activo': 'Estado'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Validar que las contraseñas coincidan si se proporcionaron
        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('Las contraseñas no coinciden')
        
        # Si es un nuevo usuario, la contraseña es obligatoria
        if not self.instance.pk and not password:
            raise forms.ValidationError('La contraseña es obligatoria para nuevos usuarios')
        
        return cleaned_data
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        
        # Si se proporcionó una contraseña, hashearla
        password = self.cleaned_data.get('password')
        if password:
            usuario.clave = make_password(password)
        
        if commit:
            usuario.save()
        
        return usuario
