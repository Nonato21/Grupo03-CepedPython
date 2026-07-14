from django.urls import path
from . import views

urlpatterns = [
    path('setores/', views.listar_setores, name='listar_setores'),
    path('gerenciar_ramais/', views.gerenciar_ramais, name='gerenciar_ramais'),
    path('', views.index, name='index'),
    path("setores/cadastrar/", views.cadastrar_setores,name="cadastrar_setores"),
    path("setores/excluir/<int:id>/", views.deletar_setores,name="deletar_setores"),
    path("setores/editar/<int:id>/", views.editar_setores, name="editar_setores"),
    path('setores/visualizarramais/', views.ver_setores, name='ver_setores'),
    path('setores/gerenciar_pessoas/', views.gerenciar_pessoas, name='gerenciar_pessoas')
]
