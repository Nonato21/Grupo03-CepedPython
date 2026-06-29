from django.shortcuts import render

# Create your views here.

from .models import Setor

def listar_setores(request):
    setores = Setor.objects.all() # Descomente essa linha!
    return render(request, 'ramais/listar_setores.html', {'lista_setores': setores})

def gerenciar_ramais(request):
    return render(request, 'ramais/gerenciar_ramais.html')

def index(request):
    return render(request, 'ramais/index.html')
