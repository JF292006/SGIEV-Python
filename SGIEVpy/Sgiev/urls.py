from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('index', views.index_view, name='index'),
    path('login', views.login, name='login'),
    path('admin', views.admin, name='admin'),

    #CATEGORIA
    path('list_categoria/', views.list_categoria, name='list_categoria'),
    path('registro_categoria/', views.registro_categoria, name='registro_categoria'),
    path('pre_editar_categoria/<str:id>', views.pre_editar_categoria, name="pre_editar_categoria"),
    path('editar_categoria/<str:id>', views.editar_categoria, name='editar_categoria'),
    path('eliminar_categoria/<str:id>', views.eliminar_categoria, name='eliminar_categoria'),
    
    #PRODUCTO
     path('list_producto/', views.list_producto, name='list_producto'),
    path('registro_producto/', views.registro_producto, name='registro_producto'),
    path('pre_editar_producto/<str:id>', views.pre_editar_producto, name="pre_editar_producto"),
    path('editar_producto/<str:id>', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<str:id>', views.eliminar_producto, name='eliminar_producto'),

    # Index / Landing Page
    path('', views.index_view, name='index'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    #PROVEEDOR
    path('proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('proveedores/registrar/', views.registrar_proveedor, name='registrar_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
]

