# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER
from .models import Setor, Pessoa, Usuario
def gerenciar_ramais(request):
    return render(request, 'ramais/gerenciar_ramais.html')

def gerenciar_pessoas(request):
    setores = Setor.objects.all()
    return render(request, 'ramais/gerenciar_pessoas.html', {'setores': setores})

def index(request):
    return render(request, 'ramais/index.html')

def cadastrar_setores(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        ramal = request.POST.get("ramal", "").strip()
        
        if nome == "":
            return render(request, "ramais/gerenciar_ramais.html", {
                "nome": nome, "email": email, "ramal": ramal,
                "erro_nome": "Informe o nome do setor"
            })
        
        if email == "":
            return render(request, "ramais/gerenciar_ramais.html", {
                "nome": nome, "email": email, "ramal": ramal,
                "erro_email": "Informe o e-mail do setor"
            })
        
        if ramal == "":
            return render(request, "ramais/gerenciar_ramais.html", {
                "nome": nome, "email": email, "ramal": ramal,
                "erro_ramal": "Informe o número do ramal"
            })
        
        if Setor.objects.filter(nome__iexact=nome).exists():
            messages.error(request, "Setor já cadastrado anteriormente, por favor adicione outro setor!")
            return render(request, "ramais/gerenciar_ramais.html", {
                "nome": nome, "email": email, "ramal": ramal
            })
            
        if Setor.objects.filter(email__iexact=email).exists():
            messages.error(request, "E-mail já cadastrado!")
            return render(request, "ramais/gerenciar_ramais.html", {
                "nome": nome, "email": email, "ramal": ramal 
            })
        
        if Setor.objects.filter(ramal=ramal).exists():
            messages.error(request, "Ramal já cadastrado!")
            return render(request, "ramais/gerenciar_ramais.html", {
                "nome": nome, "email": email, "ramal": ramal 
            })  
        
        if len(ramal) != 4:      
            messages.error(request, "O ramal deve ter exatamente 4 dígitos!")
            return render(request, "ramais/gerenciar_ramais.html", {
                "nome": nome, "email": email, "ramal": ramal 
            })
        
        Setor.objects.create(
            nome=nome,
            email=email,
            ramal=ramal
        )
        
        messages.success(request, f"Setor '{nome}' cadastrado com sucesso!")
        return redirect("cadastrar_setores")

    return render(request, "ramais/gerenciar_ramais.html")

def ver_setores(request):
    busca = request.GET.get("q", "").strip()

    setores = Setor.objects.all().order_by("nome")

    if busca:
        setores = setores.filter(
            Q(nome__icontains=busca)
            | Q(email__icontains=busca)
            | Q(ramal__icontains=busca)
        )

    return render(
        request,
        "ramais/ver_setores.html",
        {
            "lista_setores": setores
        }
    )


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
    
    pessoas = Pessoa.objects.all().prefetch_related('setores').distinct() 

    if busca:
        pessoas = pessoas.filter(
            Q(nome__icontains=busca) | 
            Q(email__icontains=busca) | 
            Q(setores__nome__icontains=busca)
        ).distinct()
    
    return render(request, 'ramais/listar_pessoas.html', {'lista_pessoas': pessoas})

def cadastrar_pessoa(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        
        if not nome or not email:
            messages.error(request, "Nome e E-mail são campos obrigatórios!")
            return render(request, "ramais/gerenciar_pessoas.html", {'nome': nome, 'email': email})

        if Pessoa.objects.filter(email__iexact=email).exists():
            messages.error(request, "Este e-mail já está cadastrado para outra pessoa!")
            return render(request, "ramais/gerenciar_pessoas.html", {'nome': nome, 'email': email})

        Pessoa.objects.create(nome=nome, email=email)
        
        messages.success(request, f"{nome} foi cadastrado(a) com sucesso!")
        
        return redirect("cadastrar_pessoa")

    return render(request, "ramais/gerenciar_pessoas.html")

def editar_pessoa(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()

        contexto = {
            "pessoa": pessoa,
            "nome": nome,
            "email": email,
        }

        if not nome or not email:
            messages.error(
                request,
                "Nome e e-mail são obrigatórios."
            )

            return render(
                request,
                "ramais/editar_pessoa.html",
                contexto
            )

        email_ja_utilizado = Pessoa.objects.filter(
            email__iexact=email
        ).exclude(
            id=id
        ).exists()

        if email_ja_utilizado:
            messages.error(
                request,
                "Este e-mail já está cadastrado para outra pessoa."
            )

            return render(
                request,
                "ramais/editar_pessoa.html",
                contexto
            )

        pessoa.nome = nome
        pessoa.email = email
        pessoa.save()

        messages.success(
            request,
            "Pessoa atualizada com sucesso!"
        )

        return redirect("listar_pessoas")

    return render(
        request,
        "ramais/editar_pessoa.html",
        {
            "pessoa": pessoa
        }
    )

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


#usuarios

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'ramais/listar_usuarios.html', {'lista_usuarios': usuarios})

def cadastrar_usuario(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "")
        confirmar_senha = request.POST.get("confirmar_senha", "")
        status_usuario = request.POST.get("status_usuario", "")
        nivel_acesso = request.POST.get("nivel_acesso", "")

        contexto = {
            'nome': nome, 'email': email, 'status_usuario': status_usuario, 'nivel_acesso': nivel_acesso
        }

        if not nome or not email or not senha:
            messages.error(request, "Nome, E-mail e Senha são obrigatórios!")
            return render(request, "ramais/gerenciar_usuarios.html", contexto)

        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem!")
            return render(request, "ramais/gerenciar_usuarios.html", contexto)

        if Usuario.objects.filter(email__iexact=email).exists():
            messages.error(request, "Este e-mail já está em uso por outro usuário!")
            return render(request, "ramais/gerenciar_usuarios.html", contexto)

        Usuario.objects.create(
            nome=nome,
            email=email,
            senha=senha,
            status_usuario=status_usuario,
            nivel_acesso=nivel_acesso
        )

        messages.success(request, f"Usuário '{nome}' cadastrado com sucesso!")
        return redirect("gerenciar_usuarios")

    return render(request, 'ramais/gerenciar_usuarios.html')

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    contexto = {
        "usuario": usuario,
        "nome": usuario.nome,
        "email": usuario.email,
        "status_usuario": usuario.status_usuario,
        "nivel_acesso": usuario.nivel_acesso,
    }

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "")
        confirmar_senha = request.POST.get(
            "confirmar_senha",
            "",
        )
        status_usuario = request.POST.get(
            "status_usuario",
            "",
        ).strip()
        nivel_acesso = request.POST.get(
            "nivel_acesso",
            "",
        ).strip()

        contexto.update({
            "nome": nome,
            "email": email,
            "status_usuario": status_usuario,
            "nivel_acesso": nivel_acesso,
        })

        if not nome or not email:
            messages.error(
                request,
                "Nome e e-mail são obrigatórios!",
            )

            return render(
                request,
                "ramais/editar_usuario.html",
                contexto,
            )

        email_em_uso = Usuario.objects.filter(
            email__iexact=email
        ).exclude(
            id=id
        ).exists()

        if email_em_uso:
            messages.error(
                request,
                "Este e-mail já está em uso por outro usuário!",
            )

            return render(
                request,
                "ramais/editar_usuario.html",
                contexto,
            )

        if status_usuario not in {"Ativo", "Inativo"}:
            messages.error(
                request,
                "Status de usuário inválido!",
            )

            return render(
                request,
                "ramais/editar_usuario.html",
                contexto,
            )

        niveis_validos = {
            "Administrador",
            "Usuário padrão",
        }

        if nivel_acesso not in niveis_validos:
            messages.error(
                request,
                "Nível de acesso inválido!",
            )

            return render(
                request,
                "ramais/editar_usuario.html",
                contexto,
            )

        if senha or confirmar_senha:

            if senha != confirmar_senha:
                messages.error(
                    request,
                    "As senhas não coincidem!",
                )

                return render(
                    request,
                    "ramais/editar_usuario.html",
                    contexto,
                )

            usuario.senha = senha

        usuario.nome = nome
        usuario.email = email
        usuario.status_usuario = status_usuario
        usuario.nivel_acesso = nivel_acesso

        usuario.save()

        messages.success(
            request,
            f"Usuário '{nome}' atualizado com sucesso!",
        )

        return redirect("listar_usuarios")

    return render(
        request,
        "ramais/editar_usuario.html",
        contexto,
    )

def deletar_usuario(request, id):
    if request.method == "POST":
        usuario = get_object_or_404(
            Usuario,
            id=id,
        )

        nome = usuario.nome

        usuario.delete()

        messages.success(
            request,
            f"Usuário '{nome}' excluído com sucesso!",
        )

    return redirect("listar_usuarios")

# VINCULOS
def gerenciar_vinculos(request):
    lista_setores = Setor.objects.all().order_by('nome')
    setor_selecionado = request.GET.get('setor_id')
    
    pessoas_do_setor = []
    pessoas_disponiveis = [] 

    if setor_selecionado:
        try:
            setor = Setor.objects.get(id=setor_selecionado)
            pessoas_do_setor = setor.pessoas.all()
            
            pessoas_disponiveis = Pessoa.objects.exclude(setores__id=setor.id).order_by('nome')
        except Setor.DoesNotExist:
            setor_selecionado = None

    contexto = {
        'lista_setores': lista_setores,
        'setor_selecionado': str(setor_selecionado) if setor_selecionado else None,
        'pessoas_do_setor': pessoas_do_setor,
        'pessoas_disponiveis': pessoas_disponiveis,
    }

    return render(request, 'ramais/gerenciar_vinculos.html', contexto)

def adicionar_vinculo(request):
    if request.method == "POST":
        setor_id = request.POST.get('setor_id')
        pessoa_id = request.POST.get('pessoa_id')

        if setor_id and pessoa_id:
            setor = Setor.objects.get(id=setor_id)
            pessoa = Pessoa.objects.get(id=pessoa_id)
            
            pessoa.setores.add(setor)
            
            messages.success(request, f"'{pessoa.nome}' foi adicionado(a) ao setor com sucesso!")
            
            url_retorno = reverse('gerenciar_vinculos') + f'?setor_id={setor.id}'
            return redirect(url_retorno)
            
    return redirect('gerenciar_vinculos')

def exportar_setores_pdf(request):
    # Receber resposta em HTTP
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachament; filename="listagem_setores.pdf"'
    
    #documento PDF
    pdf= SimpleDocTemplate(response, pagesize=A4)
    
    elementos = []
    
    #titulo do PDF
    
    estilos = getSampleStyleSheet()
    
    titulo = estilos["Heading1"]
    titulo.alignment = TA_CENTER
    
    elementos.append(Paragraph("IFMG - Campus São João Evangelista", titulo))
    elementos.append(Paragraph("Lista de ramais", titulo))
    elementos.append(Paragraph("<br/><br/>", titulo))
    
    
    #passando os dados
    
    dados = []
    
    dados.append([
        "ID",
        "Nome",
        "E-mail",
        "Ramal"
    ])
    
    setores = Setor.objects.all()
    
    for setor in setores:
        
        dados.append([
            setor.id,
            setor.nome,
            setor.email,
            setor.ramal
        ])

    #criar a tabela
    
    tabela = Table(dados)
    
    tabela.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,0),12),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige)

    ]))

    elementos.append(tabela)

    pdf.build(elementos)

    return response


def exportar_pessoas_pdf(request):
    # Receber resposta em HTTP
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachament; filename="listagem_pessoas.pdf"'
    
    #documento PDF
    pdf= SimpleDocTemplate(response, pagesize=A4)
    
    elementos = []
    
    #titulo do PDF
    
    estilos = getSampleStyleSheet()
    
    titulo = estilos["Heading1"]
    titulo.alignment = TA_CENTER
    
    elementos.append(Paragraph("IFMG - Campus São João Evangelista", titulo))
    elementos.append(Paragraph("Lista de ramais", titulo))
    elementos.append(Paragraph("<br/><br/>", titulo))
    
    
    #passando os dados
    
    dados = []
    
    dados.append([
        "ID",
        "Nome",
        "E-mail",
        "Setor Vinculado"
    ])
    
    pessoas = Pessoa.objects.all()

    for pessoa in pessoas:

        setores = ", ".join(
            setor.nome for setor in pessoa.setores.all()
        )

        dados.append([
            pessoa.id,
            pessoa.nome,
            pessoa.email,
            setores
        ])

    #criar a tabela
    
    tabela = Table(dados)
    
    tabela.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,0),12),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige)

    ]))

    elementos.append(tabela)

    pdf.build(elementos)

    return response


def exportar_usuarios_pdf(request):
    # Receber resposta em HTTP
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachament; filename="listagem_usuarios.pdf"'
    
    #documento PDF
    pdf= SimpleDocTemplate(response, pagesize=A4)
    
    elementos = []
    
    #titulo do PDF
    
    estilos = getSampleStyleSheet()
    
    titulo = estilos["Heading1"]
    titulo.alignment = TA_CENTER
    
    elementos.append(Paragraph("IFMG - Campus São João Evangelista", titulo))
    elementos.append(Paragraph("Lista de pessoas", titulo))
    elementos.append(Paragraph("<br/><br/>", titulo))
    
    
    #passando os dados
    
    dados = []
    
    dados.append([
        "ID",
        "Nome",
        "E-mail",
        "Status",
        "Nível"
    ])
    
    usuarios = Usuario.objects.all()
    
    for usuario in usuarios:
        
        dados.append([
            usuario.id,
            usuario.nome,
            usuario.email,
            usuario.status_usuario,
            usuario.nivel_acesso
            
        ])

    #criar a tabela
    
    tabela = Table(dados)
    
    tabela.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,0),12),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige)

    ]))

    elementos.append(tabela)

    pdf.build(elementos)

    return response