# 📞 Lista Telefônica - IFMG Campus São João Evangelista

Sistema web para consulta e gerenciamento de ramais telefônicos, setores e contatos internos do **IFMG Campus São João Evangelista**. Desenvolvido como parte do estágio do programa **Bolsa Futuro Digital — CEPEDI — Curso Python** (Grupo 3).

## 🚀 Funcionalidades

- Página inicial com navegação e cards informativos
- Listagem de setores com ID, Nome, E-mail e Ramal
- Cadastro de novos setores via formulário
- Painel administrativo Django para gerenciamento completo dos dados
- Layout responsivo com Bootstrap 5

## 🛠️ Tecnologias

- **Python 3.10+**
- **Django 6.0.6**
- **SQLite**
- **ReportLab 4.x**
- **Bootstrap 5.3.8**
- **HTML5 / CSS3**

## 📁 Estrutura do Projeto

```
Grupo03-CepedPython/
└── lista_telefonica/
    ├── manage.py
    ├── requirements.txt
    ├── lista_telefonica/        # Configurações do projeto Django
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    └── ramais/                  # App principal
        ├── models.py            # Modelos: Setor, Pessoa
        ├── views.py             # Lógica das páginas
        ├── urls.py              # Rotas da aplicação
        ├── admin.py             # Registro dos modelos no admin
        ├── migrations/          # Migrações do banco de dados
        ├── templates/ramais/    # Templates HTML
        └── static/ramais/       # Arquivos estáticos (CSS, imagens)
```

## ⚙️ Como executar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Grupo03-CepedPython.git
cd Grupo03-CepedPython/lista_telefonica

# Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/macOS

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Crie um superusuário para acesso administrativo
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

## 📌 Rotas

| URL | Descrição | Requer Login |
|-----|-----------|--------------|
| `/` | Página inicial | Não |
| `/setores/visualizarramais/` | Consulta pública de ramais | Não |
| `/setores/` | Gerenciar setores | Sim |
| `/setores/cadastrar/` | Cadastrar setor | Sim |
| `/pessoas/cadastrar/` | Cadastrar pessoa | Sim |
| `/pessoas/listar/` | Listar pessoas | Sim |
| `/vinculos/gerenciar/` | Gerenciar vínculos | Sim |
| `/admin/` | Painel administrativo Django | Sim |
| `/login/` | Login | - |

## 🗄️ Modelos de Dados

- **Setor** — nome (único), e-mail (único), ramal (único, 4 dígitos)
- **Pessoa** — nome, e-mail (único), setores (ManyToMany)

## 📄 Licença

Este projeto é parte do estágio do programa Bolsa Futuro Digital — CEPEDI.
