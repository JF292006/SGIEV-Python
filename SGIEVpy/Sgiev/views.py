from django.shortcuts import render, redirect
from datetime import datetime
from . models import Categoria

#VISTAS PRINCIPALES

def index(request):
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



