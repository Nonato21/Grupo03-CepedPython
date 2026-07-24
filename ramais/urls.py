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
    # path('setores/gerenciar_pessoas/', views.gerenciar_pessoas, name='gerenciar_pessoas'),

    # pessoas
    path('setores/gerenciar_pessoas/', views.gerenciar_pessoas, name='gerenciar_pessoas'),
    path('pessoas/listar/', views.listar_pessoas, name='listar_pessoas'),
    path('pessoas/cadastrar/', views.cadastrar_pessoa, name='cadastrar_pessoa'),
    path('pessoas/editar/<int:id>/', views.editar_pessoa, name='editar_pessoa'),
    path('pessoas/excluir/<int:id>/', views.deletar_pessoa, name='deletar_pessoa'),

    # usuarios
    # path('usuarios/listar/',views.listar_usuarios,name='listar_usuarios'),
    # path('usuarios/cadastrar/',views.cadastrar_usuario,name='gerenciar_usuarios'),
    # path('usuarios/editar/<int:id>/',views.editar_usuario,name='editar_usuario'),
    # path('usuarios/excluir/<int:id>/',views.deletar_usuario,name='deletar_usuario'),
    
    # vinculos
    path("vinculos/gerenciar/",views.gerenciar_vinculos,name="gerenciar_vinculos"),
    path("vinculos/adicionar/",views.adicionar_vinculo,name="adicionar_vinculo"),
    path('vinculos/remover/<int:setor_id>/<int:pessoa_id>/', views.remover_vinculo, name='remover_vinculo'),

    #exportar em pdf
    path("setores/exportar/pdf/", views.exportar_setores_pdf, name="exportar_setores_pdf"),
    path("pessoas/exportar/pdf/", views.exportar_pessoas_pdf, name="exportar_pessoas_pdf"),
    # path("usuarios/exportar/pdf/", views.exportar_usuarios_pdf, name="exportar_usuarios_pdf")
]
