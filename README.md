<div align="center">
  <h1>📞 Lista Telefônica</h1>
  <p><strong>Sistema de Gerenciamento de Ramais e Contatos</strong></p>
  <p>IFMG Campus São João Evangelista — CEPEDI — Bolsa Futuro Digital</p>
</div>

---

## 📋 Sobre o Projeto

Sistema web desenvolvido em **Django** para consulta e gerenciamento de ramais telefônicos, setores, pessoas e vínculos institucionais do **IFMG Campus São João Evangelista**. O projeto foi realizado como parte do programa **Bolsa Futuro Digital — CEPEDI — Curso Python** (Grupo 3).

### 🎯 Objetivos

- Centralizar a consulta de ramais institucionais em um único sistema
- Permitir o cadastro e gerenciamento de setores, pessoas e vínculos
- Oferecer autenticação e níveis de acesso para administradores
- Exportar listagens em PDF para consulta offline
- Disponibilizar uma interface amigável e responsiva

---

## ✨ Funcionalidades

### 🔓 Acesso Público
- Página inicial com cards informativos e navegação
- Consulta de ramais por setor com busca em tempo real

### 🔐 Acesso Administrativo (requer login)
- **Setores**: cadastrar, editar, listar, excluir e visualizar ramais
- **Pessoas**: cadastrar, editar, listar e excluir contatos
- **Vínculos**: associar ou remover pessoas a setores
- **Usuários**: gerenciar contas de acesso ao sistema
- **Exportação**: gerar PDFs com listagem de setores e pessoas

### ⚙️ Painel Administrativo Django
- Gerenciamento completo de todos os modelos via `/admin/`

---

## 🛠️ Tecnologias

| Tecnologia | Versão |
|------------|--------|
| [Python](https://www.python.org/) | 3.10+ |
| [Django](https://www.djangoproject.com/) | 6.0+ |
| [SQLite](https://www.sqlite.org/) | — |
| [ReportLab](https://www.reportlab.com/) | 4.x |
| [Bootstrap](https://getbootstrap.com/) | 5.3.8 |
| HTML5 / CSS3 | — |

---

## 📂 Estrutura do Projeto

```
Grupo03-CepedPython/
├── .gitignore
├── requirements.txt
├── README.md
├── manage.py                  # Gerenciamento do Django
├── lista_telefonica/          # Configurações do projeto
│   ├── __init__.py
│   ├── settings.py            # Configurações gerais
│   ├── urls.py                # Rotas principais
│   ├── wsgi.py                # Servidor WSGI
│   ├── asgi.py                # Servidor ASGI
│   └── BD/                    # Artefatos do banco de dados
└── ramais/                    # App principal
    ├── __init__.py
    ├── admin.py               # Registro no admin
    ├── apps.py                # Configuração do app
    ├── models.py              # Modelos: Setor, Pessoa
    ├── views.py               # Lógica das views
    ├── urls.py                # Rotas da aplicação
    ├── tests.py               # Testes
    ├── migrations/            # Migrações do banco
    ├── static/ramais/         # Arquivos estáticos (CSS, imagens)
    └── templates/ramais/      # Templates HTML
        ├── base.html
        ├── index.html
        ├── login.html
        ├── ver_setores.html
        ├── listar_setores.html
        ├── gerenciar_ramais.html
        ├── editar_ramais.html
        ├── listar_pessoas.html
        ├── gerenciar_pessoas.html
        ├── editar_pessoa.html
        ├── gerenciar_vinculos.html
        ├── listar_usuarios.html
        ├── gerenciar_usuarios.html
        └── editar_usuario.html
```

---

## 🧠 Modelos de Dados

### `Setor`
| Campo | Tipo | Restrições |
|-------|------|------------|
| `nome` | `CharField(100)` | Único, obrigatório |
| `email` | `EmailField` | Único, obrigatório |
| `ramal` | `CharField(4)` | Único, 4 dígitos numéricos |

### `Pessoa`
| Campo | Tipo | Restrições |
|-------|------|------------|
| `nome` | `CharField(100)` | Obrigatório |
| `email` | `EmailField` | Único, obrigatório |
| `setores` | `ManyToManyField(Setor)` | Relação N:N |

---

## 🗺️ Rotas

### Públicas
| URL | Descrição |
|-----|-----------|
| `/` | Página inicial |
| `/setores/visualizarramais/` | Consulta pública de ramais |

### Autenticação
| URL | Descrição |
|-----|-----------|
| `/login/` | Login |
| `/logout/` | Logout |

### Administrativas (requer login)
| URL | Descrição |
|-----|-----------|
| `/admin/` | Painel administrativo Django |
| `/setores/` | Listar setores |
| `/setores/cadastrar/` | Cadastrar setor |
| `/setores/editar/<id>/` | Editar setor |
| `/setores/excluir/<id>/` | Excluir setor |
| `/setores/exportar/pdf/` | Exportar setores em PDF |
| `/gerenciar_ramais/` | Gerenciar ramais |
| `/pessoas/cadastrar/` | Cadastrar pessoa |
| `/pessoas/listar/` | Listar pessoas |
| `/pessoas/editar/<id>/` | Editar pessoa |
| `/pessoas/excluir/<id>/` | Excluir pessoa |
| `/pessoas/exportar/pdf/` | Exportar pessoas em PDF |
| `/vinculos/gerenciar/` | Gerenciar vínculos |
| `/vinculos/adicionar/` | Adicionar vínculo |
| `/vinculos/remover/<setor_id>/<pessoa_id>/` | Remover vínculo |
| `/usuarios/listar/` | Listar usuários |
| `/usuarios/cadastrar/` | Cadastrar usuário |
| `/usuarios/editar/<id>/` | Editar usuário |
| `/usuarios/excluir/<id>/` | Excluir usuário |

---

## ⚙️ Como Executar

### Pré-requisitos
- Python 3.10 ou superior instalado
- Git instalado

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/Grupo03-CepedPython.git
cd Grupo03-CepedPython

# 2. Crie e ative um ambiente virtual
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
# source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute as migrações do banco de dados
python manage.py migrate

# 5. Crie um superusuário para acesso administrativo
python manage.py createsuperuser

# 6. Inicie o servidor de desenvolvimento
python manage.py runserver
```

Acesse [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/) no navegador.

---

## 📦 Dependências

```
Django>=6.0,<7.0
reportlab>=4.0,<5.0
```

---

## 🤝 Contribuição

Projeto desenvolvido para fins educacionais no âmbito do programa **Bolsa Futuro Digital — CEPEDI**.

### Equipe (Grupo 3)
- [@Saas]
- [Nonato]
- [@Getulio]
- [@rafael]
- [@Claudia]
- [@Abelardo] — *

---

## 📄 Licença

Este projeto é de caráter educacional, desenvolvido como parte do estágio do programa **Bolsa Futuro Digital — CEPEDI — Curso Python**.

---

<div align="center">
  <p>IFMG Campus São João Evangelista — 2025</p>
</div>
