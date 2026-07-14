# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Setor, Pessoa
from django.db.models import Q

def listar_setores(request):
    setores = Setor.objects.all() # Descomente essa linha!
    return render(request, 'ramais/listar_setores.html', {'lista_setores': setores})

def gerenciar_ramais(request):
    return render(request, 'ramais/gerenciar_ramais.html')

def gerenciar_pessoas(request):
    setores = Setor.objects.all()
    return render(request, 'ramais/gerenciar_pessoas.html', {'setores': setores})

def index(request):
    return render(request, 'ramais/index.html')

def cadastrar_setores(request):

    if request.method == "POST":

        nome = request.POST["nome"].strip()
        email = request.POST["email"].strip()
        ramal = request.POST["ramal"].strip()
    
               
        if nome == "":
            return render(request,
                          "ramais/gerenciar_ramais.html",
                          {
                              "nome":nome,
                              "email":email,
                              "ramal":ramal,
                              "erro_nome": "Informe o nome do setor"
                          })
        
        if email == "":
            return render(request,
                          "ramais/gerenciar_ramais.html",
                          {
                              "nome":nome,
                              "email":email,
                              "ramal":ramal,
                              "erro_email": "Informe o nome do e-mail"
                          })
        
        if ramal == "":
            return render(request,
                          "ramais/gerenciar_ramais.html",
                          {
                              "nome":nome,
                              "email":email,
                              "ramal":ramal,
                              "erro_ramal": "Informe o número do ramal"
                          })
        
        if Setor.objects.filter(nome__iexact=nome).exists():
            messages.error(request, "Setor já cadastrado anteriormente, por favor adicione outro setor!!!")
            return render(request,
                          "ramais/gerenciar_ramais.html",
                          {
                            "nome": nome,
                            "email":email,
                            "ramal":ramal   
                          })
            
            
        if Setor.objects.filter(email__iexact=email).exists():
            messages.error(request, "E-mail já cadastrado")
            return render(request,
                          "ramais/gerenciar_ramais.html",
                          {
                            "nome": nome,
                            "email":email,
                            "ramal":ramal   
                          })
        
        if Setor.objects.filter(ramal=ramal).exists():
            messages.error(request, "Ramal já cadastrado")
            return render(request, "ramais/gerenciar_ramais.html", 
                          {
                            "nome": nome,
                            "email":email,
                            "ramal":ramal   
                          })  
        
        if(len(ramal)!=4):      
            messages.error(request, "O ramal deve ter exatamente 4 digitos!!!")
            return render(request, "ramais/gerenciar_ramais.html", 
                          {
                            "nome": nome,
                            "email":email,
                            "ramal":ramal   
                          })
        
        Setor.objects.create(
            nome=nome,
            email=email,
            ramal=ramal
        )
        
        messages.success(request, "Setor cadastrado com sucesso!!!")
        

        return redirect("listar_setores")

    return render(request, "ramais/gerenciar_ramais.html")

def ver_setores(request):
    setores = Setor.objects.all()
    return render(request, 'ramais/ver_setores.html', {'lista_setores': setores})


#CRUDs
def deletar_setores(request, id):
    
    if request.method == "POST":
        
        setor = get_object_or_404(Setor, id=id)
        
        setor.delete()
        
        messages.success(request, "Setor excluído com sucesso!!!")
        
    return redirect("listar_setores")
    
def editar_setores(request, id):
    
    setor = get_object_or_404(Setor, id=id)
    
    if request.method == "POST":
        nome = request.POST["nome"].strip()
        email = request.POST["email"].strip()
        ramal = request.POST["ramal"].strip()       
                
        if nome == "":
            return render(request,
                          "ramais/editar_ramais.html",
                          { 
                              "setor":setor,
                              "nome":nome,
                              "email":email,
                              "ramal":ramal,
                              "erro_nome": "Informe o nome do setor"
                          })
        
        if email == "":
            return render(request,
                          "ramais/editar_ramais.html",
                          {
                              "setor":setor,
                              "nome":nome,
                              "email":email,
                              "ramal":ramal,
                              "erro_email": "Informe o nome do e-mail"
                          })
        
        if ramal == "":
            return render(request,
                          "ramais/editar_ramais.html",
                          {
                              "setor":setor,
                              "nome":nome,
                              "email":email,
                              "ramal":ramal,
                              "erro_ramal": "Informe o número do ramal"
                          })
        
        if Setor.objects.filter(nome__iexact=nome).exclude(id=id).exists():
            messages.error(request, "Setor já cadastrado anteriormente, por favor adicione outro setor!")
            return render(request,
                          "ramais/editar_ramais.html",
                          {
                            "setor":setor,
                            "nome": nome,
                            "email":email,
                            "ramal":ramal   
                          })
            
            
        if Setor.objects.filter(email__iexact=email).exclude(id=id).exists():
            messages.error(request, "E-mail já cadastrado!!!")
            return render(request,
                          "ramais/editar_ramais.html",
                          {
                            "setor":setor,
                            "nome": nome,
                            "email":email,
                            "ramal":ramal   
                          })
        
        if Setor.objects.filter(ramal=ramal).exclude(id=id).exists():
            messages.error(request, "Ramal já cadastrado!!!")
            return render(request, "ramais/editar_ramais.html", 
                          {
                            "setor":setor,  
                            "nome": nome,
                            "email":email,
                            "ramal":ramal   
                          })  
        
        if(len(ramal)!=4):      
            messages.error(request, "O ramal deve ter exatamente 4 digitos!!!")
            return render(request, "ramais/editar_ramais.html", 
                          {
                            "setor":setor,
                            "nome": nome,
                            "email":email,
                            "ramal":ramal   
                          })
        
        setor.nome = nome
        setor.email = email
        setor.ramal = ramal
        
        setor.save()              
        
        messages.success(request, "Setor atualizado com sucesso!!!")
        
        return redirect("listar_setores")

    return render(request, "ramais/editar_ramais.html",
                  {
                    "setor":setor
                    })

def listar_pessoas(request):
    busca = request.GET.get('q')
    # O select_related otimiza a busca no banco quando usamos ForeignKey
    pessoas = Pessoa.objects.all().select_related('setor') 

    if busca:
        pessoas = pessoas.filter(
            Q(nome__icontains=busca) | 
            Q(email__icontains=busca) | 
            Q(ramal__icontains=busca) |
            Q(setor__nome__icontains=busca) # Permite buscar pelo nome do setor!
        )
    
    return render(request, 'ramais/listar_pessoas.html', {'lista_pessoas': pessoas})

def cadastrar_pessoa(request):
    setores = Setor.objects.all()

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        ramal = request.POST.get("ramal", "").strip()
        setor_id = request.POST.get("setor") # Captura o ID do setor escolhido no <select>
        
        if not nome or not ramal or not setor_id:
            messages.error(request, "Nome, Ramal e Setor são campos obrigatórios!")
            return render(request, "ramais/gerenciar_pessoas.html", {'setores': setores})
        
        if len(ramal) != 4:
            messages.error(request, "O ramal deve ter exatamente 4 dígitos!")
            return render(request, "ramais/gerenciar_pessoas.html", {'setores': setores})

        if Pessoa.objects.filter(ramal=ramal).exists():
            messages.error(request, "Este ramal já está em uso por outra pessoa!")
            return render(request, "ramais/gerenciar_pessoas.html", {'setores': setores})

        setor_selecionado = get_object_or_404(Setor, id=setor_id)

        Pessoa.objects.create(
            nome=nome,
            email=email,
            ramal=ramal,
            setor=setor_selecionado
        )
        
        messages.success(request, "Pessoa cadastrada com sucesso!")
        return redirect("listar_pessoas")

    return render(request, "ramais/gerenciar_pessoas.html", {'setores': setores})

def editar_pessoa(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)
    setores = Setor.objects.all()

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        ramal = request.POST.get("ramal", "").strip()
        setor_id = request.POST.get("setor")
        
        if not nome or not ramal or not setor_id:
            messages.error(request, "Nome, Ramal e Setor são obrigatórios!")
            return render(request, "ramais/editar_pessoa.html", {'pessoa': pessoa, 'setores': setores})
            
        if len(ramal) != 4:
            messages.error(request, "O ramal deve ter exatamente 4 dígitos!")
            return render(request, "ramais/editar_pessoa.html", {'pessoa': pessoa, 'setores': setores})

        if Pessoa.objects.filter(ramal=ramal).exclude(id=id).exists():
            messages.error(request, "Este ramal já está em uso!")
            return render(request, "ramais/editar_pessoa.html", {'pessoa': pessoa, 'setores': setores})

        setor_selecionado = get_object_or_404(Setor, id=setor_id)
        pessoa.nome = nome
        pessoa.email = email
        pessoa.ramal = ramal
        pessoa.setor = setor_selecionado
        
        pessoa.save()
        
        messages.success(request, "Contato atualizado com sucesso!")
        return redirect("listar_pessoas")

    return render(request, "ramais/editar_pessoa.html", {'pessoa': pessoa, 'setores': setores})

def deletar_pessoa(request, id):
    if request.method == "POST":
        pessoa = get_object_or_404(Pessoa, id=id)
        pessoa.delete()
        messages.success(request, "Contato excluído com sucesso!")
    return redirect("listar_pessoas")

# Barra de pesquisa
def listar_setores(request):
    busca = request.GET.get('q')
    setores = Setor.objects.all()

    if busca:
        setores = setores.filter(
            Q(nome__icontains=busca) | 
            Q(email__icontains=busca) | 
            Q(ramal__icontains=busca)
        )
    return render(request, 'ramais/listar_setores.html', {'lista_setores': setores})
