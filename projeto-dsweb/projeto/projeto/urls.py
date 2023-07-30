"""
URL configuration for projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from simulados import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('simulados/', views.listar_simulados, name='listar_simulados'),
    path('criar-questao/', views.criar_questao, name='criar_questao'),
    path('criar-simulado/', views.criar_simulado, name='criar_simulado'),
    
    path('detalhes-simulados/<int:simulado_id>/', views.detalhes_simulado, name='detalhes_simulado'),

    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('processar-respostas/', views.processar_respostas, name='processar_respostas'),

    path('cadastro/', views.cadastro, name='cadastro'),
]
