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
- **MySQL**
- **Bootstrap 5.3.8**
- **HTML5 / CSS3**

## 📁 Estrutura do Projeto

```
Grupo03-CepedPython/
└── lista_telefonica/
    ├── manage.py
    ├── lista_telefonica/        # Configurações do projeto Django
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    └── ramais/                  # App principal
        ├── models.py            # Modelos: Setor, Pessoa, Usuario
        ├── views.py             # Lógica das páginas
        ├── urls.py              # Rotas da aplicação
        ├── admin.py             # Registro dos modelos no admin
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
pip install django mysqlclient

# Configure o banco MySQL em lista_telefonica/settings.py
# (database: lista_telefonica, user: root, password: root, host: localhost)

# Execute as migrações
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

## 📌 Rotas

| URL | Descrição |
|-----|-----------|
| `/` | Página inicial |
| `/setores/` | Listagem de setores |
| `/gerenciar/` | Cadastro de setores |
| `/admin/` | Painel administrativo |

## 🗄️ Modelos de Dados

- **Setor** — nome, e-mail, ramal
- **Pessoa** — nome, e-mail, setores (ManyToMany)
- **Usuario** — nome, e-mail (único), senha, status, nível de acesso

## 📄 Licença

Este projeto é parte do estágio do programa Bolsa Futuro Digital — CEPEDI.
