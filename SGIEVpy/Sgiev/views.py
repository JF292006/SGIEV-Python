from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models, transaction
from django.http import JsonResponse
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from .models import (
    Categoria, 
    Proveedor,
    Usuarios, 
    Producto, 
    Venta, 
    Venta_has_producto, 
    Movimiento_inventario,
    Envio, 
    Mensajeria
)
from .forms import LoginForm, UsuarioForm, VentaForm, AgregarProductoForm,EditarEstadoVentaForm,EnvioForm, MensajeriaForm
from .decorators import admin_required



def index(request):  
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


# CATEGORIA

def inicio_cat(request):
    return render(request, 'categoria/index.html')


def list_categoria(request):
    categoria = Categoria.objects.all()
    data = {'categoria': categoria}
    return render(request, 'categoria/index.html', data)


def registro_categoria(request):
    if request.method == "POST":
        nombre = request.POST.get('nombreCat')
        descripcion = request.POST.get('descCat')
        fecha = datetime.now()
        estado = 1

        categoria = Categoria(
            nombre_categoria=nombre,
            descripcion_categoria=descripcion,
            fecha_creacion=fecha,
            activo=estado
        )
        
        categoria.save()
        return redirect('list_categoria')
    return render(request, 'categoria/nuevocat.html')


def pre_editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    data = {
        'categoria': categoria
    }
    return render(request, 'categoria/editarcat.html', data)


def editar_categoria(request, id):
    if request.method == "POST":
        categoria = Categoria.objects.get(id=id)

        nombre = request.POST.get('nombreCat')
        descripcion = request.POST.get('descCat')
        estado = request.POST.get('estadoCat')

        categoria.nombre_categoria = nombre
        categoria.descripcion_categoria = descripcion
        categoria.activo = estado

        categoria.save()
    return redirect("categoria/index")


def eliminar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
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
        registro_sanitario = request.POST.get('registrosanitario')
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
        producto.registrosaniario = request.POST.get('registrosanitario')

        
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

#VENTA DE PROVEEDOR
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

@login_required
@transaction.atomic
def crear_compra_proveedor(request, idproveedor):
    proveedor = get_object_or_404(Proveedor, id=idproveedor)
    productos = Producto.objects.filter(activo=1)

    if request.method == "POST":
        print("POST RECIBIDO:", request.POST)

        tipo = request.POST.get("tipo_producto")
        estado = request.POST.get("estado_compra", "pendiente")
        observaciones = request.POST.get("observaciones", "")
        numero_factura = request.POST.get("numero_factura", "")

        cantidad = int(request.POST.get("cantidad", "0"))
        precio_unitario = Decimal(request.POST.get("valor_unitario") or "0")
        subtotal_linea = cantidad * precio_unitario
        iva = subtotal_linea * Decimal("0.19")
        total = subtotal_linea + iva

        # --- SI EL PRODUCTO ES NUEVO ---
        if tipo == "nuevo":
            producto = Producto.objects.create(
                nombre_producto=request.POST.get('nombre_producto'),
                descripcion_producto=request.POST.get('descripcion_producto', ''),
                codigo_barras=request.POST.get('codigo_barras', ''),
                registrosaniario=request.POST.get('registrosaniario', ''),
                precio_compra=precio_unitario,
                precio_venta=Decimal(request.POST.get('precio_venta') or '0'),
                margen_ganancia=Decimal('0'),
                stock_actual=0,
                stock_minimo=int(request.POST.get('stock_minimo') or 1),
                stock_maximo=int(request.POST.get('stock_maximo') or 1000),
                fecha_vencimiento=request.POST.get('fecha_vencimiento') or None,
                categoria_idcategoria_id=request.POST.get('categoria'),
                proveedor_idproveedor=proveedor,
                activo=1
            )
        else:
            producto = get_object_or_404(Producto, id=request.POST.get("producto_id"))

        # crear compra principal
        compra = Compra_proveedor.objects.create(
            numero_factura_compra=numero_factura if numero_factura else f"CMP{Compra_proveedor.objects.count()+1}",
            subtotal_compra=subtotal_linea,
            iva_compra=iva,
            total_compra=total,
            estado_compra=estado,
            observaciones_compra=observaciones,
            imagen_factura_compra="",  # no viene en el formulario
            usuarios_id_usuario=request.user,
            producto_idproducto=producto
        )

        # crear detalle
        Compra_detalle.objects.create(
            compra_idcompra=compra,
            producto_idproducto=producto,
            cantidad=cantidad,
            precio_compra_unitario=precio_unitario,
            subtotal_linea_compra=subtotal_linea,
            lote=request.POST.get("lote", ""),
            fecha_vencimiento=request.POST.get("fecha_vencimiento") or None
        )

        # actualizar stock
        producto.stock_actual += cantidad
        producto.precio_compra = precio_unitario
        producto.save()

        messages.success(request, "Compra registrada exitosamente.")
        return redirect("listar_proveedores")

    return render(request, "proveedor/crear_compra.html", {
        "proveedor": proveedor,
        "productos": productos,
    })



#PROVEEDOR

def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor/listar_prov.html', {'proveedores': proveedores})

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


# ===== VISTAS DE USUARIOS (CRUD) =====

@admin_required
def usuarios_listar(request):
    """
    Lista todos los usuarios con paginación y búsqueda
    """
    # Obtener parámetro de búsqueda
    search = request.GET.get('search', '')
    
    # Filtrar usuarios
    if search:
        usuarios = Usuarios.objects.filter(
            models.Q(p_nombre__icontains=search) |
            models.Q(p_apellido__icontains=search) |
            models.Q(correo__icontains=search) |
            models.Q(num_identificacion__icontains=search)
        ).order_by('-fecha_registro')
    else:
        usuarios = Usuarios.objects.all().order_by('-fecha_registro')
    
    # Paginación
    paginator = Paginator(usuarios, 10)  # 10 usuarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'usuario': request.user
    }
    
    return render(request, 'usuarios/listar.html', context)


@admin_required
def usuarios_crear(request):
    """
    Crear un nuevo usuario
    """
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('usuarios_listar')
    else:
        form = UsuarioForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Usuario',
        'usuario': request.user
    }
    
    return render(request, 'usuarios/crear.html', context)


@admin_required
def usuarios_editar(request, id):
    """
    Editar un usuario existente
    """
    usuario = get_object_or_404(Usuarios, pk=id)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente')
            return redirect('usuarios_listar')
    else:
        form = UsuarioForm(instance=usuario)
    
    context = {
        'form': form,
        'titulo': 'Editar Usuario',
        'usuario': request.user,
        'usuario_editando': usuario
    }
    
    return render(request, 'usuarios/editar.html', context)


@admin_required
def usuarios_eliminar(request, id):
    """
    Eliminar (desactivar) un usuario
    """
    usuario = get_object_or_404(Usuarios, pk=id)
    
    # No permitir eliminar al usuario actual
    if usuario.id == request.user.id:
        messages.error(request, 'No puedes eliminar tu propio usuario')
        return redirect('usuarios_listar')
    
    # Desactivar en lugar de eliminar
    usuario.activo = 0
    usuario.save()
    
    messages.success(request, f'Usuario {usuario.nombre_completo} desactivado exitosamente')
    return redirect('usuarios_listar')


@admin_required
def usuarios_detalle(request, id):
    """
    Ver detalles de un usuario
    """
    usuario_detalle = get_object_or_404(Usuarios, pk=id)
    
    context = {
        'usuario_detalle': usuario_detalle,
        'usuario': request.user
    }
    
    return render(request, 'usuarios/detalle.html', context)


# ===== VISTAS DE VENTAS =====

@login_required(login_url='login')
def ventas_listar(request):
    """
    Lista todas las ventas con filtros
    - Administrador: ve todas las ventas
    - Operario: solo ve sus propias ventas
    """
    # Filtros
    search = request.GET.get('search', '')
    estado = request.GET.get('estado', '')
    metodo = request.GET.get('metodo', '')
    
    # Query base según el rol
    if request.user.tipo_usu == 'administrador':
        # Admin ve todas las ventas
        ventas = Venta.objects.all().order_by('-fecha_factura')
    else:
        # Operario solo ve sus ventas
        ventas = Venta.objects.filter(usuarios_id_usuario=request.user).order_by('-fecha_factura')
    
    # Aplicar filtros
    if search:
        ventas = ventas.filter(
            models.Q(numero_factura__icontains=search) |
            models.Q(usuarios_id_usuario__p_nombre__icontains=search) |
            models.Q(usuarios_id_usuario__p_apellido__icontains=search)
        )
    
    if estado:
        ventas = ventas.filter(estado_pago=estado)
    
    if metodo:
        ventas = ventas.filter(metodo_pago=metodo)
    
    # Paginación - CAMBIAR A 10 REGISTROS
    paginator = Paginator(ventas, 10)  # Cambiar de 15 a 10
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'estado': estado,
        'metodo': metodo,
        'usuario': request.user,
        'es_admin': request.user.tipo_usu == 'administrador'
    }
    
    return render(request, 'ventas/listar.html', context)


@login_required(login_url='login')
def ventas_crear(request):
    """
    Crear nueva venta con sistema de carrito
    """
    if request.method == 'POST':
        if 'finalizar_venta' in request.POST:
            # Finalizar venta
            return procesar_venta(request)
        else:
            # Agregar producto al carrito
            return agregar_al_carrito(request)
    
    # GET - Mostrar formulario
    venta_form = VentaForm()
    producto_form = AgregarProductoForm()
    
    # Obtener carrito de la sesión
    carrito = request.session.get('carrito_venta', [])
    
    # Calcular totales
    subtotal = sum(Decimal(str(item['subtotal'])) for item in carrito)
    
    context = {
        'venta_form': venta_form,
        'producto_form': producto_form,
        'carrito': carrito,
        'subtotal': subtotal,
        'usuario': request.user,
        'es_admin': request.user.tipo_usu == 'administrador'
    }
    
    return render(request, 'ventas/crear.html', context)


def agregar_al_carrito(request):
    """
    Agrega un producto al carrito de la sesión
    """
    producto_form = AgregarProductoForm(request.POST)
    
    if producto_form.is_valid():
        producto = producto_form.cleaned_data['producto']
        cantidad = producto_form.cleaned_data['cantidad']
        
        # Obtener o crear carrito
        carrito = request.session.get('carrito_venta', [])
        
        # Verificar si el producto ya está en el carrito
        producto_existente = False
        for item in carrito:
            if item['producto_id'] == producto.id:
                # Actualizar cantidad
                nueva_cantidad = item['cantidad'] + cantidad
                if nueva_cantidad <= producto.stock_actual:
                    item['cantidad'] = nueva_cantidad
                    item['subtotal'] = float(producto.precio_venta * nueva_cantidad)
                    item['stock_disponible'] = producto.stock_actual  # Actualizar stock
                    producto_existente = True
                    messages.success(request, f'Cantidad actualizada: {producto.nombre_producto}')
                else:
                    messages.error(request, f'Stock insuficiente para {producto.nombre_producto}')
                    return redirect('ventas_crear')
                break
        
        if not producto_existente:
            # Agregar nuevo producto
            carrito.append({
                'producto_id': producto.id,
                'nombre': producto.nombre_producto,
                'precio': float(producto.precio_venta),
                'cantidad': cantidad,
                'subtotal': float(producto.precio_venta * cantidad),
                'stock_disponible': producto.stock_actual,
                'stock_minimo': producto.stock_minimo  # AGREGAR ESTO
            })
            messages.success(request, f'Producto agregado: {producto.nombre_producto}')
        
        # Guardar carrito en sesión
        request.session['carrito_venta'] = carrito
        request.session.modified = True
    else:
        for error in producto_form.errors.values():
            messages.error(request, error)
    
    return redirect('ventas_crear')


@login_required(login_url='login')
def ventas_quitar_producto(request, producto_id):
    """
    Quita un producto del carrito
    """
    carrito = request.session.get('carrito_venta', [])
    carrito = [item for item in carrito if item['producto_id'] != producto_id]
    request.session['carrito_venta'] = carrito
    request.session.modified = True
    
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('ventas_crear')


@login_required(login_url='login')
def ventas_limpiar_carrito(request):
    """
    Limpia todo el carrito
    """
    request.session['carrito_venta'] = []
    request.session.modified = True
    
    messages.success(request, 'Carrito vaciado')
    return redirect('ventas_crear')


@transaction.atomic
def procesar_venta(request):
    """
    Procesa la venta final: crea la venta, descuenta inventario y registra movimientos
    """
    venta_form = VentaForm(request.POST)
    carrito = request.session.get('carrito_venta', [])
    
    if not carrito:
        messages.error(request, 'El carrito está vacío')
        return redirect('ventas_crear')
    
    if venta_form.is_valid():
        try:
            # Calcular totales
            subtotal = sum(Decimal(str(item['subtotal'])) for item in carrito)
            descuento = venta_form.cleaned_data['descuento'] or Decimal('0')
            iva = (subtotal - descuento) * Decimal('0.19')  # IVA 19%
            valor_total = subtotal - descuento + iva
            abono = venta_form.cleaned_data['abono'] or Decimal('0')
            saldo_pendiente = valor_total - abono
            
            # Crear venta
            venta = venta_form.save(commit=False)
            venta.subtotal = subtotal
            venta.iva = iva
            venta.valor_total = valor_total
            venta.saldo_pendiente = saldo_pendiente
            venta.usuarios_id_usuario = request.user
            venta.imagen_recibo = ''
            venta.save()
            
            # Lista para productos con stock bajo
            productos_stock_bajo = []
            
            # Procesar cada producto del carrito
            for item in carrito:
                producto = Producto.objects.get(id=item['producto_id'])
                cantidad = item['cantidad']
                
                # Verificar stock nuevamente
                if producto.stock_actual < cantidad:
                    raise Exception(f'Stock insuficiente para {producto.nombre_producto}')
                
                # Crear detalle de venta
                Venta_has_producto.objects.create(
                    venta_idfactura=venta,
                    producto_idproducto=producto,
                    cantidad=cantidad,
                    valor_unitario=producto.precio_venta,
                    subtotal_linea=Decimal(str(item['subtotal']))
                )
                
                # Actualizar stock
                stock_anterior = producto.stock_actual
                producto.stock_actual -= cantidad
                producto.save()
                
                # VERIFICAR STOCK BAJO DESPUÉS DE LA VENTA
                if producto.stock_actual <= producto.stock_minimo:
                    productos_stock_bajo.append({
                        'nombre': producto.nombre_producto,
                        'stock_actual': producto.stock_actual,
                        'stock_minimo': producto.stock_minimo
                    })
                
                # Registrar movimiento de inventario
                Movimiento_inventario.objects.create(
                    tipo_movimiento='venta',
                    cantidad=cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=producto.stock_actual,
                    precio_unitario=producto.precio_venta,
                    valor_total=Decimal(str(item['subtotal'])),
                    referencia_id=venta.id,
                    tipo_referencia='venta',
                    observaciones=f'Venta #{venta.numero_factura}',
                    imagen_comprobante='',
                    usuarios_id_usuario=request.user,
                    producto_idproducto=producto
                )
            
            # Limpiar carrito
            request.session['carrito_venta'] = []
            request.session.modified = True
            
            # Mensajes de éxito y alertas
            messages.success(request, f'Venta {venta.numero_factura} registrada exitosamente')
            
            # Alertar sobre productos con stock bajo
            if productos_stock_bajo:
                for prod in productos_stock_bajo:
                    messages.warning(
                        request, 
                        f'⚠️ ALERTA: {prod["nombre"]} tiene stock bajo. '
                        f'Actual: {prod["stock_actual"]} | Mínimo: {prod["stock_minimo"]}'
                    )
            
            return redirect('ventas_detalle', id=venta.id)
            
        except Exception as e:
            messages.error(request, f'Error al procesar la venta: {str(e)}')
            return redirect('ventas_crear')
    else:
        for error in venta_form.errors.values():
            messages.error(request, error)
        return redirect('ventas_crear')


@login_required(login_url='login')
def ventas_detalle(request, id):
    """
    Ver detalles completos de una venta (factura)
    """
    venta = get_object_or_404(Venta, pk=id)
    productos = Venta_has_producto.objects.filter(venta_idfactura=venta)
    
    context = {
        'venta': venta,
        'productos': productos,
        'usuario': request.user,
        'es_admin': request.user.tipo_usu == 'administrador'
    }
    
    return render(request, 'ventas/detalle.html', context)


@login_required(login_url='login')
def obtener_precio_producto(request, producto_id):
    """
    API para obtener información de un producto (AJAX)
    """
    try:
        producto = Producto.objects.get(id=producto_id, activo=1)
        data = {
            'precio': float(producto.precio_venta),
            'stock': producto.stock_actual,
            'nombre': producto.nombre_producto
        }
        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

@admin_required
def ventas_editar_estado(request, id):
    """
    Permite al administrador editar solo el estado de pago de una venta
    """
    venta = get_object_or_404(Venta, pk=id)
    
    if request.method == 'POST':
        form = EditarEstadoVentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, f'Estado de la venta {venta.numero_factura} actualizado')
            return redirect('ventas_detalle', id=venta.id)
    else:
        form = EditarEstadoVentaForm(instance=venta)
    
    context = {
        'form': form,
        'venta': venta,
        'usuario': request.user,
        'es_admin': True
    }
    
    return render(request, 'ventas/editar_estado.html', context)


@login_required(login_url='login')
def ventas_generar_pdf(request, id):
    """
    Genera un PDF de la factura de venta
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from django.http import HttpResponse
    from io import BytesIO
    
    # Obtener la venta
    venta = get_object_or_404(Venta, pk=id)
    productos = Venta_has_producto.objects.filter(venta_idfactura=venta)
    
    # Crear el objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{venta.numero_factura}.pdf"'
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#3d862e'),
        alignment=TA_CENTER
    )
    
    # Título
    elements.append(Paragraph("ROMAR NATURAL", title_style))
    elements.append(Paragraph("NIT: 52101085", styles['Normal']))
    elements.append(Paragraph("Teléfono: 3053615676", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Información de la factura
    elements.append(Paragraph(f"<b>FACTURA: {venta.numero_factura}</b>", styles['Heading2']))
    elements.append(Paragraph(f"Fecha: {venta.fecha_factura.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Paragraph(f"Vendedor: {venta.usuarios_id_usuario.nombre_completo}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de productos
    data = [['#', 'Producto', 'Cant.', 'Precio Unit.', 'Subtotal']]
    
    for idx, item in enumerate(productos, 1):
        data.append([
            str(idx),
            item.producto_idproducto.nombre_producto[:30],
            str(item.cantidad),
            f"${item.valor_unitario:,.0f}",
            f"${item.subtotal_linea:,.0f}"
        ])
    
    # Crear tabla
    table = Table(data, colWidths=[0.5*inch, 3*inch, 0.8*inch, 1.2*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3d862e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Totales
    totales_data = [
        ['Subtotal:', f"${venta.subtotal:,.0f}"],
        ['Descuento:', f"-${venta.descuento:,.0f}"],
        ['IVA (19%):', f"${venta.iva:,.0f}"],
        ['<b>TOTAL:</b>', f"<b>${venta.valor_total:,.0f}</b>"]
    ]
    
    if venta.abono > 0:
        totales_data.append(['Abono:', f"${venta.abono:,.0f}"])
        totales_data.append(['<b>Saldo Pendiente:</b>', f"<b>${venta.saldo_pendiente:,.0f}</b>"])
    
    totales_table = Table(totales_data, colWidths=[3*inch, 2*inch])
    totales_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 14),
        ('LINEABOVE', (0, -2), (-1, -2), 2, colors.black),
    ]))
    
    elements.append(totales_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Información adicional
    elements.append(Paragraph(f"<b>Método de Pago:</b> {venta.get_metodo_pago_display()}", styles['Normal']))
    elements.append(Paragraph(f"<b>Estado:</b> {venta.get_estado_pago_display()}", styles['Normal']))
    
    if venta.observaciones:
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(f"<b>Observaciones:</b> {venta.observaciones}", styles['Normal']))
    
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Gracias por su compra", styles['Normal']))
    
    # Construir PDF
    doc.build(elements)
    
    # Obtener el valor del buffer y escribirlo en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
@admin_required
@transaction.atomic
def ventas_eliminar(request, id):
    """
    Elimina una venta y devuelve el stock al inventario
    Solo disponible para administradores
    """
    venta = get_object_or_404(Venta, pk=id)
    
    try:
        # Obtener todos los productos de la venta
        productos_venta = Venta_has_producto.objects.filter(venta_idfactura=venta)
        
        # Revertir el stock de cada producto
        for item in productos_venta:
            producto = item.producto_idproducto
            cantidad = item.cantidad
            
            # Devolver el stock
            stock_anterior = producto.stock_actual
            producto.stock_actual += cantidad
            producto.save()
            
            # Registrar movimiento de reversión
            Movimiento_inventario.objects.create(
                tipo_movimiento='ajuste',
                cantidad=cantidad,
                stock_anterior=stock_anterior,
                stock_nuevo=producto.stock_actual,
                precio_unitario=producto.precio_venta,
                valor_total=item.subtotal_linea,
                referencia_id=venta.id,
                tipo_referencia='ajuste',
                observaciones=f'Reversión por eliminación de venta {venta.numero_factura}',
                imagen_comprobante='',
                usuarios_id_usuario=request.user,
                producto_idproducto=producto
            )
        
        # Guardar información antes de eliminar
        numero_factura = venta.numero_factura
        
        # Eliminar la venta (esto eliminará también los detalles por CASCADE)
        venta.delete()
        
        messages.success(
            request, 
            f'Venta {numero_factura} eliminada exitosamente. El stock ha sido devuelto al inventario.'
        )
        
    except Exception as e:
        messages.error(request, f'Error al eliminar la venta: {str(e)}')
    
    return redirect('ventas_listar')

# ===== VISTAS DE MENSAJERÍA (SOLO ADMIN) =====

@admin_required
def mensajeria_listar(request):
    """
    Lista todas las empresas de mensajería (solo admin)
    """
    search = request.GET.get('search', '')
    
    if search:
        mensajerias = Mensajeria.objects.filter(
            models.Q(nombre_mensajeria__icontains=search) |
            models.Q(cobertura__icontains=search)
        ).order_by('nombre_mensajeria')
    else:
        mensajerias = Mensajeria.objects.all().order_by('nombre_mensajeria')
    
    paginator = Paginator(mensajerias, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'usuario': request.user,
        'es_admin': True
    }
    
    return render(request, 'mensajeria/listar.html', context)


@admin_required
def mensajeria_crear(request):
    """
    Crear nueva empresa de mensajería (solo admin)
    """
    if request.method == 'POST':
        form = MensajeriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa de mensajería creada exitosamente')
            return redirect('mensajeria_listar')
    else:
        form = MensajeriaForm()
    
    context = {
        'form': form,
        'titulo': 'Nueva Empresa de Mensajería',
        'usuario': request.user,
        'es_admin': True
    }
    
    return render(request, 'mensajeria/crear.html', context)


@admin_required
def mensajeria_editar(request, id):
    """
    Editar empresa de mensajería (solo admin)
    """
    mensajeria = get_object_or_404(Mensajeria, pk=id)
    
    if request.method == 'POST':
        form = MensajeriaForm(request.POST, instance=mensajeria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa de mensajería actualizada exitosamente')
            return redirect('mensajeria_listar')
    else:
        form = MensajeriaForm(instance=mensajeria)
    
    context = {
        'form': form,
        'titulo': 'Editar Empresa de Mensajería',
        'mensajeria': mensajeria,
        'usuario': request.user,
        'es_admin': True
    }
    
    return render(request, 'mensajeria/editar.html', context)


@admin_required
def mensajeria_eliminar(request, id):
    """
    Eliminar empresa de mensajería (solo admin)
    """
    mensajeria = get_object_or_404(Mensajeria, pk=id)
    nombre = mensajeria.nombre_mensajeria
    mensajeria.delete()
    
    messages.success(request, f'Empresa {nombre} eliminada exitosamente')
    return redirect('mensajeria_listar')


# ===== VISTAS DE ENVÍOS =====

@login_required(login_url='login')
def envios_listar(request):
    """
    Lista todos los envíos
    Admin: ve todos | Operario: ve los suyos
    """
    search = request.GET.get('search', '')
    estado = request.GET.get('estado', '')
    
    # Filtrar según rol
    if request.user.tipo_usu == 'administrador':
        envios = Envio.objects.all().order_by('-fecha_envio')
    else:
        envios = Envio.objects.filter(usuarios_id_usuario=request.user).order_by('-fecha_envio')
    
    # Aplicar filtros
    if search:
        envios = envios.filter(
            models.Q(venta_idfactura__numero_factura__icontains=search) |
            models.Q(direccion_envio__icontains=search) |
            models.Q(fk_mensajeria__nombre_mensajeria__icontains=search)
        )
    
    if estado:
        envios = envios.filter(estado_envio=estado)
    
    paginator = Paginator(envios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'estado': estado,
        'usuario': request.user,
        'es_admin': request.user.tipo_usu == 'administrador'
    }
    
    return render(request, 'envios/listar.html', context)


@login_required(login_url='login')
def envios_crear(request):
    """
    Crear nuevo envío
    """
    if request.method == 'POST':
        form = EnvioForm(request.POST)
        if form.is_valid():
            envio = form.save(commit=False)
            envio.usuarios_id_usuario = request.user
            envio.save()
            messages.success(request, f'Envío registrado exitosamente')
            return redirect('envios_detalle', id=envio.id)
    else:
        form = EnvioForm()
    
    context = {
        'form': form,
        'titulo': 'Registrar Nuevo Envío',
        'usuario': request.user,
        'es_admin': request.user.tipo_usu == 'administrador'
    }
    
    return render(request, 'envios/crear.html', context)


@login_required(login_url='login')
def envios_editar(request, id):
    """
    Editar envío existente
    """
    envio = get_object_or_404(Envio, pk=id)
    
    if request.method == 'POST':
        form = EnvioForm(request.POST, instance=envio)  # ← instance=envio es crucial
        if form.is_valid():
            form.save()
            messages.success(request, 'Envío actualizado exitosamente')
            return redirect('envios_detalle', id=envio.id)
    else:
        form = EnvioForm(instance=envio)  # ← instance=envio autocompleta
    
    context = {
        'form': form,
        'titulo': 'Editar Envío',
        'envio': envio,
        'usuario': request.user,
        'es_admin': request.user.tipo_usu == 'administrador'
    }
    
    return render(request, 'envios/editar.html', context)


@admin_required
def envios_eliminar(request, id):
    """
    Eliminar envío (solo admin)
    """
    envio = get_object_or_404(Envio, pk=id)
    factura = envio.venta_idfactura.numero_factura
    envio.delete()
    
    messages.success(request, f'Envío de la factura {factura} eliminado exitosamente')
    return redirect('envios_listar')


@login_required(login_url='login')
def envios_detalle(request, id):
    """
    Ver detalles de un envío
    """
    envio = get_object_or_404(Envio, pk=id)
    
    context = {
        'envio': envio,
        'usuario': request.user,
        'es_admin': request.user.tipo_usu == 'administrador'
    }
    
    return render(request, 'envios/detalle.html', context)
