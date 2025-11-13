from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('admin', views.admin, name='admin'),

    #CATEGORIA
    path('list_categoria/', views.list_categoria, name='list_categoria'),
    path('registro_categoria/', views.registro_categoria, name='registro_categoria'),
    path('pre_editar_categoria/<str:id>', views.pre_editar_categoria, name="pre_editar_categoria"),
    path('editar_categoria/<str:id>', views.editar_categoria, name='editar_categoria'),
    path('eliminar_categoria/<str:id>', views.eliminar_categoria, name='eliminar_categoria'),
    

    # Index / Landing Page
    path('', views.index, name='index'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
]

