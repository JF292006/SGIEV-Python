from django.shortcuts import render, redirect, get_object_or_404

from datetime import datetime
from . models import Categoria, Producto
from .models import Proveedor

#VISTAS PRINCIPALES

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .models import Usuarios



def index_view(request):
    """
    Vista principal - Landing page
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def admin(request):
    return render(request, 'admin.html')


#CATEGORIA

def inicio_cat(request):
    return render (request, 'categoria/index.html')

def list_categoria(request):
    categoria = Categoria.objects.all()
    data={'categoria':categoria}
    return render (request, 'categoria/index.html', data)

def registro_categoria(request):
    if request.method=="POST":
        nombre = request.POST.get('nombreCat')
        descripcion = request.POST.get('descCat')
        fecha = datetime.now()
        estado = 1

        categoria=Categoria(nombre_categoria=nombre,
                            descripcion_categoria=descripcion, 
                            fecha_creacion=fecha,
                            activo=estado)
        
        categoria.save()
        return redirect('list_categoria')
    return render(request, 'categoria/nuevocat.html')

def pre_editar_categoria(request, id):
    categoria=Categoria.objects.get(id=id)
    data={
        'categoria':categoria
    }
    return render(request, 'categoria/editarcat.html', data)

def editar_categoria(request, id):
    if request.method=="POST":
        categoria=Categoria.objects.get(id=id)

        nombre = request.POST.get('nombreCat')
        descripcion = request.POST.get('descCat')
        estado = request.POST.get('estadoCat')

        categoria.nombre_categoria=nombre
        categoria.descripcion_categoria=descripcion
        categoria.activo=estado

        categoria.save()
    return redirect("categoria/index")


def eliminar_categoria(request, id):
    categoria=Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('list_categoria')

#PRODUCTOS

def list_producto(request):
    producto = Producto.objects.select_related('categoria_idcategoria', 'proveedor_idproveedor').all()
    data = {'producto': producto}
    return render(request, 'producto/index.html', data)


def registro_producto(request):
    if request.method == "POST":
        
        nombre = request.POST.get('nombre_producto')
        descripcion = request.POST.get('descripcion_producto')
        codigo = request.POST.get('codigo_barras')
        registro_sanitario = request.POST.get('registrosaniario')
        precio_compra = request.POST.get('precio_compra') or "0"
        precio_venta = request.POST.get('precio_venta') or "0"
        margen = request.POST.get('margen_ganancia') or "0"
        stock_actual = request.POST.get('stock_actual') or "0"
        stock_min = request.POST.get('stock_minimo') or "0"
        stock_max = request.POST.get('stock_maximo') or "0"
        fecha_ven = request.POST.get('fecha_vencimiento')
        fecha_cre = datetime.now()
        categoria_id = request.POST.get('categoria_idcategoria')
        proveedor_id = request.POST.get('proveedor_idproveedor')
        activo = request.POST.get('activo') or 1

        
        try:
            precio_compra = Decimal(precio_compra)
        except InvalidOperation:
            precio_compra = Decimal('0.00')
        try:
            precio_venta = Decimal(precio_venta)
        except InvalidOperation:
            precio_venta = Decimal('0.00')
        try:
            margen = Decimal(margen)
        except InvalidOperation:
            margen = Decimal('0.00')

        try:
            stock_actual = int(stock_actual)
        except:
            stock_actual = 0
        try:
            stock_min = int(stock_min)
        except:
            stock_min = 0
        try:
            stock_max = int(stock_max)
        except:
            stock_max = 0

       
        categoria = get_object_or_404(Categoria, id=categoria_id)
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)

        producto = Producto(
            nombre_producto = nombre,
            descripcion_producto = descripcion,
            codigo_barras = codigo,
            registrosaniario = registro_sanitario,
            precio_compra = precio_compra,
            precio_venta = precio_venta,
            margen_ganancia = margen,
            stock_actual = stock_actual,
            stock_minimo = stock_min,
            stock_maximo = stock_max,
            fecha_vencimiento = fecha_ven,
            categoria_idcategoria = categoria,
            proveedor_idproveedor = proveedor,
            activo = activo
        )
        producto.save()
        return redirect('list_producto')

  
    categorias = Categoria.objects.filter(activo=1)
    proveedores = Proveedor.objects.filter(activo=1)
    data = {'categorias': categorias, 'proveedores': proveedores}
    return render(request, 'producto/nuevoprod.html', data)



def pre_editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.filter(activo=1)
    proveedores = Proveedor.objects.filter(activo=1)
    data = {
        'producto': producto,
        'categorias': categorias,
        'proveedores': proveedores
    }
    return render(request, 'producto/editarprod.html', data)



def editar_producto(request, id):
    if request.method == "POST":
        producto = get_object_or_404(Producto, id=id)

        producto.nombre_producto = request.POST.get('nombre_producto')
        producto.descripcion_producto = request.POST.get('descripcion_producto')
        producto.codigo_barras = request.POST.get('codigo_barras')
        producto.registrosaniario = request.POST.get('registrosaniario')

        
        from decimal import Decimal, InvalidOperation
        try:
            producto.precio_compra = Decimal(request.POST.get('precio_compra') or '0')
        except InvalidOperation:
            producto.precio_compra = Decimal('0.00')
        try:
            producto.precio_venta = Decimal(request.POST.get('precio_venta') or '0')
        except InvalidOperation:
            producto.precio_venta = Decimal('0.00')
        try:
            producto.margen_ganancia = Decimal(request.POST.get('margen_ganancia') or '0')
        except InvalidOperation:
            producto.margen_ganancia = Decimal('0.00')

        try:
            producto.stock_actual = int(request.POST.get('stock_actual') or 0)
        except:
            producto.stock_actual = 0
        try:
            producto.stock_minimo = int(request.POST.get('stock_minimo') or 0)
        except:
            producto.stock_minimo = 0
        try:
            producto.stock_maximo = int(request.POST.get('stock_maximo') or 0)
        except:
            producto.stock_maximo = 0

        producto.fecha_vencimiento = request.POST.get('fecha_vencimiento')

        
        categoria_id = request.POST.get('categoria_idcategoria')
        proveedor_id = request.POST.get('proveedor_idproveedor')
        producto.categoria_idcategoria = get_object_or_404(Categoria, id=categoria_id)
        producto.proveedor_idproveedor = get_object_or_404(Proveedor, id=proveedor_id)

        producto.activo = request.POST.get('activo') or producto.activo

        producto.save()

    return redirect('list_producto')


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('list_producto')


#LOGIN - AUTENTICACIÓN 

def login_view(request):
    """
    Vista para login de usuarios - SIN usar django.contrib.auth.login()
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            
            # Autenticar usando el backend personalizado
            user = authenticate(request, correo=correo, password=password)
            
            if user is not None:
                # Crear sesión manualmente sin disparar señales
                request.session['_auth_user_id'] = user.pk
                request.session['_auth_user_backend'] = 'Sgiev.backends.UsuariosBackend'
                request.session.save()
                
                # Mensaje de bienvenida
                messages.success(request, f'Bienvenido {user.p_nombre} {user.p_apellido}')
                
                # Redirigir al dashboard
                return redirect('dashboard')
            else:
                messages.error(request, 'Credenciales inválidas')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """
    Vista para cerrar sesión
    """
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('index')


@login_required(login_url='login')
def dashboard_view(request):
    """
    Vista principal del dashboard
    """
    context = {
        'usuario': request.user,
        'es_admin': request.user.tipo_usu == 'administrador',
        'es_operario': request.user.tipo_usu == 'operario'
    }
    return render(request, 'dashboard.html', context)

   
#PROVEEDOR

def registrar_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_proveedor')
        correo = request.POST.get('correo_proveedor')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        nit = request.POST.get('nit')
        contacto_nombre = request.POST.get('contacto_nombre')
        contacto_telefono = request.POST.get('contacto_telefono')
        activo = request.POST.get('activo')

        proveedor = Proveedor(
            nombre_proveedor=nombre,
            correo_proveedor=correo,
            telefono=telefono,
            direccion=direccion,
            nit=nit,
            contacto_nombre=contacto_nombre,
            contacto_telefono=contacto_telefono,
            activo=1 if activo == 'on' else 0
        )
        proveedor.save()

        return redirect('listar_proveedores')  # Redirige al listado al terminar
    return render(request, 'proveedor/registrarprov.html')

def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor/listar_prov.html', {'proveedores': proveedores})

def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)

    if request.method == 'POST':
        proveedor.nombre_proveedor = request.POST['nombre_proveedor']
        proveedor.correo_proveedor = request.POST['correo_proveedor']
        proveedor.telefono = request.POST['telefono']
        proveedor.direccion = request.POST['direccion']
        proveedor.nit = request.POST['nit']
        proveedor.contacto_nombre = request.POST['contacto_nombre']
        proveedor.contacto_telefono = request.POST['contacto_telefono']
        proveedor.activo = 1 if request.POST.get('activo') == 'True' else 0
        proveedor.save()
        return redirect('listar_proveedores')

    return render(request, 'proveedor/editar_proveedor.html', {'proveedor': proveedor})

def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    proveedor.delete()
    return redirect('listar_proveedores')

