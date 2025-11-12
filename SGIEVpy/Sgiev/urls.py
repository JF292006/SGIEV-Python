from django.urls import path
from . import views

urlpatterns = [
    # Index / Landing Page
    path('', views.index_view, name='index'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
