from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuarios, Venta, Producto, Venta_has_producto
from decimal import Decimal


class EditarEstadoVentaForm(forms.ModelForm):
    """
    Formulario para que admin edite solo el estado de pago de una venta
    """
    class Meta:
        model = Venta
        fields = ['estado_pago']
        
        widgets = {
            'estado_pago': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            })
        }
        
        labels = {
            'estado_pago': 'Estado de Pago'
        }

class VentaForm(forms.ModelForm):
    """
    Formulario para registrar ventas
    """
    class Meta:
        model = Venta
        fields = [
            'numero_factura',
            'descuento',
            'metodo_pago',
            'estado_pago',
            'abono',
            'observaciones'
        ]
        
        widgets = {
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de factura (ej: FAC-001)',
                'required': 'required'
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'value': '0',
                'step': '0.01',
                'min': '0'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'estado_pago': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'abono': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'value': '0',
                'step': '0.01',
                'min': '0'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales',
                'rows': 3
            })
        }
        
        labels = {
            'numero_factura': 'Número de Factura',
            'descuento': 'Descuento ($)',
            'metodo_pago': 'Método de Pago',
            'estado_pago': 'Estado de Pago',
            'abono': 'Abono Inicial ($)',
            'observaciones': 'Observaciones'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generar número de factura automático si es nuevo
        if not self.instance.pk:
            ultima_venta = Venta.objects.all().order_by('-id').first()
            if ultima_venta:
                try:
                    num = int(ultima_venta.numero_factura.split('-')[-1]) + 1
                    self.fields['numero_factura'].initial = f'FAC-{num:05d}'
                except:
                    self.fields['numero_factura'].initial = 'FAC-00001'
            else:
                self.fields['numero_factura'].initial = 'FAC-00001'


class AgregarProductoForm(forms.Form):
    """
    Formulario para agregar productos al carrito
    """
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=1, stock_actual__gt=0),
        label='Producto',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required',
            'id': 'id_producto'
        })
    )
    
    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1',
            'value': '1',
            'min': '1',
            'id': 'id_cantidad'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el display del producto
        self.fields['producto'].label_from_instance = lambda obj: f"{obj.nombre_producto} - Stock: {obj.stock_actual} - ${obj.precio_venta}"
    
    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        
        if producto and cantidad:
            if cantidad > producto.stock_actual:
                raise forms.ValidationError(
                    f'Stock insuficiente. Disponible: {producto.stock_actual} unidades'
                )
        
        return cleaned_data

class AgregarProductoForm(forms.Form):
    """
    Formulario para agregar productos al carrito
    """
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=1, stock_actual__gt=0),
        label='Producto',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required',
            'id': 'id_producto'
        })
    )
    
    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1',
            'value': '1',
            'min': '1',
            'id': 'id_cantidad'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el display del producto
        self.fields['producto'].label_from_instance = lambda obj: f"{obj.nombre_producto} - Stock: {obj.stock_actual} - ${obj.precio_venta}"
    
    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        
        if producto and cantidad:
            if cantidad > producto.stock_actual:
                raise forms.ValidationError(
                    f'Stock insuficiente. Disponible: {producto.stock_actual} unidades'
                )
        
        return cleaned_data

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
