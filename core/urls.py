"""
URLs do app core - Sistema Lumon
"""
from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Páginas principais
    path('home/', views.home_view, name='home'),

    # Cadastros
    path('departamentos/', views.departamentos_view, name='departamentos'),
    path('usuarios/', views.usuarios_view, name='usuarios'),

    # Relatórios
    path('relatorios/usuarios-departamento/', views.relatorio_usuarios_departamento_view, name='relatorio_usuarios_departamento'),
]
