from django.shortcuts import render, redirect

from datetime import datetime
from . models import Categoria

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

