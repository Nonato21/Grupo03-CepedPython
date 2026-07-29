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
from .models import Setor, Pessoa
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


#Parte dos usuários
User = get_user_model()

@login_required
def listar_usuarios(request):
    busca = request.GET.get("q", "").strip()

    usuarios = User.objects.all().order_by(
        "first_name",
        "username",
    )

    if busca:
        usuarios = usuarios.filter(
            Q(username__icontains=busca)
            | Q(first_name__icontains=busca)
            | Q(last_name__icontains=busca)
            | Q(email__icontains=busca)
        )

    return render(
        request,
        "ramais/listar_usuarios.html",
        {
            "lista_usuarios": usuarios,
        },
    )
    

@login_required
def cadastrar_usuario(request):
    if request.method == "POST":
        username = request.POST.get(
            "username",
            "",
        ).strip()

        primeiro_nome = request.POST.get(
            "first_name",
            "",
        ).strip()

        sobrenome = request.POST.get(
            "last_name",
            "",
        ).strip()

        email = request.POST.get(
            "email",
            "",
        ).strip().lower()

        senha = request.POST.get(
            "senha",
            "",
        )

        confirmar_senha = request.POST.get(
            "confirmar_senha",
            "",
        )

        status_usuario = request.POST.get(
            "status_usuario",
            "Ativo",
        )

        contexto = {
            "username": username,
            "first_name": primeiro_nome,
            "last_name": sobrenome,
            "email": email,
            "status_usuario": status_usuario,
        }

        if not username or not primeiro_nome or not senha:
            messages.error(
                request,
                "Usuário, nome e senha são obrigatórios.",
            )

            return render(
                request,
                "ramais/gerenciar_usuarios.html",
                contexto,
            )

        if senha != confirmar_senha:
            messages.error(
                request,
                "As senhas não coincidem.",
            )

            return render(
                request,
                "ramais/gerenciar_usuarios.html",
                contexto,
            )

        if User.objects.filter(
            username__iexact=username
        ).exists():
            messages.error(
                request,
                "Este nome de usuário já está cadastrado.",
            )

            return render(
                request,
                "ramais/gerenciar_usuarios.html",
                contexto,
            )

        if email and User.objects.filter(
            email__iexact=email
        ).exists():
            messages.error(
                request,
                "Este e-mail já está cadastrado.",
            )

            return render(
                request,
                "ramais/gerenciar_usuarios.html",
                contexto,
            )

        usuario = User.objects.create_user(
            username=username,
            email=email,
            password=senha,
        )

        usuario.first_name = primeiro_nome
        usuario.last_name = sobrenome

        usuario.is_staff = True

        usuario.is_active = (
            status_usuario == "Ativo"
        )

        usuario.save()

        messages.success(
            request,
            f"Usuário '{username}' cadastrado com sucesso.",
        )

        return redirect("listar_usuarios")

    return render(
        request,
        "ramais/gerenciar_usuarios.html",
    )
    
    
@login_required
def editar_usuario(request, id):
    usuario = get_object_or_404(
        User,
        id=id,
    )

    if (
        usuario.is_superuser
        and not request.user.is_superuser
    ):
        messages.error(
            request,
            "Somente um superusuário pode editar "
            "outro superusuário.",
        )

        return redirect("listar_usuarios")

    contexto = {
        "usuario": usuario,
        "username": usuario.username,
        "first_name": usuario.first_name,
        "last_name": usuario.last_name,
        "email": usuario.email,
        "status_usuario": (
            "Ativo"
            if usuario.is_active
            else "Inativo"
        ),
    }

    if request.method == "POST":
        username = request.POST.get(
            "username",
            "",
        ).strip()

        primeiro_nome = request.POST.get(
            "first_name",
            "",
        ).strip()

        sobrenome = request.POST.get(
            "last_name",
            "",
        ).strip()

        email = request.POST.get(
            "email",
            "",
        ).strip().lower()

        senha = request.POST.get(
            "senha",
            "",
        )

        confirmar_senha = request.POST.get(
            "confirmar_senha",
            "",
        )

        status_usuario = request.POST.get(
            "status_usuario",
            "Ativo",
        )

        contexto.update({
            "username": username,
            "first_name": primeiro_nome,
            "last_name": sobrenome,
            "email": email,
            "status_usuario": status_usuario,
        })

        if not username or not primeiro_nome:
            messages.error(
                request,
                "Usuário e nome são obrigatórios.",
            )

            return render(
                request,
                "ramais/editar_usuario.html",
                contexto,
            )

        username_em_uso = User.objects.filter(
            username__iexact=username
        ).exclude(
            id=usuario.id
        ).exists()

        if username_em_uso:
            messages.error(
                request,
                "Este nome de usuário já está em uso.",
            )

            return render(
                request,
                "ramais/editar_usuario.html",
                contexto,
            )

        email_em_uso = (
            email
            and User.objects.filter(
                email__iexact=email
            ).exclude(
                id=usuario.id
            ).exists()
        )

        if email_em_uso:
            messages.error(
                request,
                "Este e-mail já está em uso.",
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
                    "As novas senhas não coincidem.",
                )

                return render(
                    request,
                    "ramais/editar_usuario.html",
                    contexto,
                )

            usuario.set_password(senha)

        usuario.username = username
        usuario.first_name = primeiro_nome
        usuario.last_name = sobrenome
        usuario.email = email

        usuario.is_staff = True

        if usuario == request.user:
            usuario.is_active = True

        elif usuario.is_superuser:
            usuario.is_active = True

        else:
            usuario.is_active = (
                status_usuario == "Ativo"
            )

        usuario.save()

        messages.success(
            request,
            "Usuário atualizado com sucesso.",
        )

        return redirect("listar_usuarios")

    return render(
        request,
        "ramais/editar_usuario.html",
        contexto,
    )
    

@login_required
def deletar_usuario(request, id):
    if request.method != "POST":
        return redirect("listar_usuarios")

    usuario = get_object_or_404(
        User,
        id=id,
    )

    if usuario == request.user:
        messages.error(
            request,
            "Você não pode excluir a própria conta.",
        )

        return redirect("listar_usuarios")

    if usuario.is_superuser:
        messages.error(
            request,
            "Um superusuário não pode ser excluído "
            "por esta página.",
        )

        return redirect("listar_usuarios")

    nome = (
        usuario.get_full_name()
        or usuario.username
    )

    usuario.delete()

    messages.success(
        request,
        f"Usuário '{nome}' excluído com sucesso.",
    )

    return redirect("listar_usuarios")


@login_required
def gerenciar_ramais(request):
    return render(request, 'ramais/gerenciar_ramais.html')

@login_required
def gerenciar_pessoas(request):
    setores = Setor.objects.all()
    return render(request, 'ramais/gerenciar_pessoas.html', {'setores': setores})

def index(request):
    return render(request, 'ramais/index.html')

@login_required
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
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "O formato do e-mail inserido é inválido!")
            return render(request, "ramais/gerenciar_ramais.html", {
                "nome": nome, "email": email, "ramal": ramal 
            })

        if not ramal.isdigit() or len(ramal) != 4:      
            messages.error(request, "O ramal deve conter exatamente 4 números!")
            return render(request, "ramais/gerenciar_ramais.html", {
                "nome": nome, "email": email, "ramal": ramal 
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

@login_required
def deletar_setores(request, id):
    
    if request.method == "POST":
        
        setor = get_object_or_404(Setor, id=id)
        
        setor.delete()
        
        messages.success(request, "Setor excluído com sucesso!!!")
        
    return redirect("listar_setores")
    
@login_required
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

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "O formato do e-mail inserido é inválido!")
            return render(request, "ramais/editar_ramais.html", {
                "setor":setor, "nome":nome, "email":email, "ramal":ramal 
            })

        if not ramal.isdigit() or len(ramal) != 4:      
            messages.error(request, "O ramal deve conter exatamente 4 números!")
            return render(request, "ramais/editar_ramais.html", {
                "setor":setor, "nome":nome, "email":email, "ramal":ramal 
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

@login_required
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

@login_required
def cadastrar_pessoa(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        
        if not nome or not email:
            messages.error(request, "Nome e E-mail são campos obrigatórios!")
            return render(request, "ramais/gerenciar_pessoas.html", {'nome': nome, 'email': email})

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "O formato do e-mail inserido é inválido!")
            return render(request, "ramais/gerenciar_pessoas.html", {'nome': nome, 'email': email})

        if Pessoa.objects.filter(email__iexact=email).exists():
            messages.error(request, "Este e-mail já está cadastrado para outra pessoa!")
            return render(request, "ramais/gerenciar_pessoas.html", {'nome': nome, 'email': email})

        Pessoa.objects.create(nome=nome, email=email)
        
        messages.success(request, f"{nome} foi cadastrado(a) com sucesso!")
        
        return redirect("cadastrar_pessoa")

    return render(request, "ramais/gerenciar_pessoas.html")

@login_required
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

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "O formato do e-mail inserido é inválido!")
            return render(request, "ramais/editar_pessoa.html", contexto)

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

@login_required
def deletar_pessoa(request, id):
    if request.method == "POST":
        pessoa = get_object_or_404(Pessoa, id=id)
        pessoa.delete()
        messages.success(request, "Contato excluído com sucesso!")
    return redirect("listar_pessoas")

@login_required
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

@login_required
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

@login_required 
def adicionar_vinculo(request):
    if request.method == "POST":
        setor_id = request.POST.get('setor_id')
        pessoa_id = request.POST.get('pessoa_id')

        if setor_id and pessoa_id:
            setor = get_object_or_404(Setor, id=setor_id)
            pessoa = get_object_or_404(Pessoa, id=pessoa_id)
            
            pessoa.setores.add(setor)
            
            messages.success(request, f"'{pessoa.nome}' foi adicionado(a) ao setor com sucesso!")
            
            url_retorno = reverse('gerenciar_vinculos') + f'?setor_id={setor.id}'
            return redirect(url_retorno)
            
    return redirect('gerenciar_vinculos')

@login_required
def remover_vinculo(request):
    if request.method == "POST":
        setor_id = request.POST.get('setor_id')
        pessoa_id = request.POST.get('pessoa_id')

        if setor_id and pessoa_id:
            setor = get_object_or_404(Setor, id=setor_id)
            pessoa = get_object_or_404(Pessoa, id=pessoa_id)

            pessoa.setores.remove(setor)

            messages.success(request, f"'{pessoa.nome}' foi removido(a) do setor com sucesso!")

            url_retorno = reverse('gerenciar_vinculos') + f'?setor_id={setor.id}'
            return redirect(url_retorno)

    return redirect('gerenciar_vinculos')

def exportar_setores_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="listagem_setores.pdf"'
    
    pdf= SimpleDocTemplate(response, pagesize=A4)
    
    elementos = []
    
    estilos = getSampleStyleSheet()
    
    titulo = estilos["Heading1"]
    titulo.alignment = TA_CENTER
    
    elementos.append(Paragraph("IFMG - Campus São João Evangelista", titulo))
    elementos.append(Paragraph("Lista de ramais", titulo))
    elementos.append(Paragraph("<br/><br/>", titulo))
    
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

@login_required
def exportar_pessoas_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="listagem_pessoas.pdf"'
    
    pdf= SimpleDocTemplate(response, pagesize=A4)
    
    elementos = []
    
    estilos = getSampleStyleSheet()
    
    titulo = estilos["Heading1"]
    titulo.alignment = TA_CENTER
    
    elementos.append(Paragraph("IFMG - Campus São João Evangelista", titulo))
    elementos.append(Paragraph("Lista de pessoas", titulo))
    elementos.append(Paragraph("<br/><br/>", titulo))
    
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
