from django.urls import path
from . import views

urlpatterns = [
    path('setores/', views.listar_setores, name='listar_setores'),
    path('gerenciar/', views.gerenciar_ramais, name='gerenciar_ramais'),
    path('', views.index, name='index'),
    # espaço para adicionar mais rotas
]
