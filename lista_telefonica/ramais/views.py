# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Setor

def listar_setores(request):
    setores = Setor.objects.all() # Descomente essa linha!
    return render(request, 'ramais/listar_setores.html', {'lista_setores': setores})

def gerenciar_ramais(request):
    return render(request, 'ramais/gerenciar_ramais.html')

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

 
    


