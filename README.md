# Sistema Lumon

Sistema de gestão de pessoal inspirado na série "Severance" (Ruptura), desenvolvido com Django para aulas de Programação WEB do Curso de Bacharelado em Engenharia de Computação.

## 📋 Sobre o Projeto

O Sistema Lumon é uma aplicação web simples de gerenciamento de funcionários, departamentos e relatórios, com interface responsiva para dispositivos de telas de qualquer tamanho.

## ✨ Funcionalidades

- Autenticação personalizada (sem django.contrib.auth)
- CRUD de Departamentos
- CRUD de Usuários com upload de fotos e crop de imagens
- Geração de relatório
- Interface responsiva com cards para mobile
- Sistema de filtros e paginação
- Upload de fotos com nomes únicos (UUID)
- Exclusão automática de arquivos ao deletar registros com Django Signals

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Django 5.2.9** - Framework web
- **PostgreSQL 17.4** - Banco de dados
- **psycopg2-binary** - Adapter/Driver PostgreSQL
- **Pillow** - Manipulação de imagens
- **python-decouple** - Gerenciamento de variáveis de ambiente

### Frontend
- **Tailwind CSS** - Framework CSS utilitário
- **Alpine.js** - Framework JavaScript reativo
- **HTMX** - Interações AJAX
- **Toastr.js** - Janelas personalizadas de notificações
- **Cropper.js** - Crop de imagens

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

### 1. Python 3.11 ou superior

**Windows:**
- Baixe em: https://www.python.org/downloads/
- Durante a instalação, marque "Add Python to PATH"

**macOS:**
```bash
# Via Homebrew
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

Verifique a instalação:
```bash
python --version
# ou
python3 --version
```

### 2. PostgreSQL 17.4 (ou superior)

**Windows:**
- Baixe em: https://www.postgresql.org/download/windows/
- Durante a instalação, anote a senha do usuário `postgres`

**macOS:**
```bash
# Via Homebrew
brew install postgresql@17
brew services start postgresql@17
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

Verifique a instalação:
```bash
psql --version
```

### 3. Git

**Windows:**
- Baixe em: https://git-scm.com/download/win

**macOS:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

## 🚀 Instalação e Configuração

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/ciniro/lumon.git
cd lumon
```

### Passo 2: Criar e Ativar o Ambiente Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Você saberá que o ambiente virtual está ativo quando ver `(venv)` no início da linha do terminal.

### Passo 3: Atualizar o pip e Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt
```

### Passo 4: Configurar o Banco de Dados PostgreSQL

#### 4.1. Acessar o PostgreSQL

**Windows:**
```bash
psql -U postgres
```

**macOS/Linux:**
```bash
sudo -u postgres psql
```

#### 4.2. Criar o Banco de Dados e Usuário

No prompt do PostgreSQL (`postgres=#`), execute:

```sql
-- Criar o banco de dados
CREATE DATABASE lumon_db;

-- Criar o usuário
CREATE USER lumon_user WITH PASSWORD 'lumon123';

-- Configurar encoding
ALTER DATABASE lumon_db OWNER TO lumon_user;

-- Dar privilégios ao usuário
GRANT ALL PRIVILEGES ON DATABASE lumon_db TO lumon_user;

-- Conectar ao banco
\c lumon_db

-- Dar privilégios no schema public (necessário para PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO lumon_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO lumon_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO lumon_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO lumon_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO lumon_user;

-- Sair
\q
```

### Passo 5: Criar o Arquivo de Configuração `.env`

Na raiz do projeto, crie um arquivo chamado `.env` com o seguinte conteúdo:

```env
# Configurações do Banco de Dados PostgreSQL
DB_NAME=lumon_db
DB_USER=lumon_user
DB_PASSWORD=lumon123
DB_HOST=localhost
DB_PORT=5432

# Chave secreta do Django (gere uma nova em: https://djecrety.ir/)
SECRET_KEY=django-insecure-6l@1^_!rp^(t&4%wx6cthy#oucx7gcqiglo(&3@g9bv#su2ubw

# Debug (True em desenvolvimento, False em produção)
DEBUG=True
```

**⚠️ IMPORTANTE:**
- Se você alterou a senha do banco de dados no Passo 4, atualize `DB_PASSWORD` aqui
- Em produção, gere uma nova `SECRET_KEY` e configure `DEBUG=False`

### Passo 6: Executar as Migrations

```bash
python manage.py migrate
```

Você verá algo como:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying core.0001_initial... OK
  ...
```

### Passo 7: Popular o Banco de Dados (Seed)

Este comando criará os perfis, departamentos e usuários iniciais com suas fotos:

```bash
python manage.py seed_database
```

Você verá:
```
Iniciando população do banco de dados...
Criando perfis...
  ✓ Perfil criado: Gerente
  ✓ Perfil criado: Funcionário
Criando departamentos...
  ✓ Departamento criado: Refinamento de Macrodados (MDR)
  ✓ Departamento criado: Bem Estar (Wellness)
  ✓ Departamento criado: Ótica e Design (O&D)
Criando usuários...
  ✓ Usuário criado: Mark Scout (mark@lumon.com)
  ...
Carregando fotos dos usuários...
  ✓ Foto carregada: Mark Scout -> usuarios/fotos/...
  ...

Resumo:
  • Perfis: 2
  • Departamentos: 3
  • Usuários: 6
  • Fotos carregadas: 6/6
```

### Passo 8: Executar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

O servidor iniciará em: **http://127.0.0.1:8000/**

## 🎯 Acessando o Sistema

### Página de Login

Acesse: http://127.0.0.1:8000/

### Usuários de Teste

Após executar o `seed_database`, você pode fazer login com:

| E-mail | Senha | Perfil | Departamento |
|--------|-------|--------|--------------|
| mark@lumon.com | 1234 | Gerente | MDR |
| helly@lumon.com | 1234 | Funcionário | MDR |
| irving@lumon.com | 1234 | Funcionário | MDR |
| dylan@lumon.com | 1234 | Funcionário | MDR |
| casey@lumon.com | 1234 | Funcionário | Wellness |
| burt@lumon.com | 1234 | Gerente | O&D |

## 📁 Estrutura do Projeto

```
sistema_lumon/
├── config/                      # Configurações do Django
│   ├── settings.py             # Configurações principais
│   ├── urls.py                 # URLs principais
│   └── wsgi.py                 # WSGI config
├── core/                        # App principal
│   ├── management/             # Commands personalizados
│   │   └── commands/
│   │       ├── seed_database.py         # Popular banco
│   │       ├── load_user_photos.py      # Carregar fotos
│   │       └── migrate_user_photos.py   # Migrar fotos
│   ├── migrations/             # Migrações do banco
│   ├── models.py               # Modelos (Perfil, Departamento, Usuario)
│   ├── views.py                # Views/Controllers
│   ├── urls.py                 # URLs do app
│   └── signals.py              # Signals (exclusão automática de fotos)
├── templates/                   # Templates HTML
│   ├── base.html               # Template base
│   ├── login.html              # Tela de login
│   ├── home.html               # Tela inicial
│   ├── departamentos.html      # CRUD de departamentos
│   ├── usuarios.html           # CRUD de usuários
│   └── relatorio_usuarios_departamento.html
├── static/                      # Arquivos estáticos
│   ├── css/                    # Estilos CSS
│   ├── js/                     # Scripts JavaScript
│   └── img/                    # Imagens e ícones
├── media/                       # Uploads de usuários
│   └── usuarios/fotos/         # Fotos dos usuários
├── manage.py                    # Gerenciador Django
├── requirements.txt             # Dependências Python
├── .env                        # Variáveis de ambiente (não versionado)
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Este arquivo
```

## 🎨 Funcionalidades Detalhadas

### 1. Sistema de Autenticação
- Autenticação personalizada sem `django.contrib.auth.User`
- Senhas hasheadas com `make_password()` e `check_password()`
- Sistema de sessões do Django

### 2. CRUD de Departamentos
- Criar, editar e excluir departamentos
- Campos: Nome completo e Sigla
- Proteção: Não permite excluir departamentos com funcionários

### 3. CRUD de Usuários
- Upload e crop de fotos com Cropper.js
- Fotos armazenadas com nomes UUID únicos
- Exclusão automática de fotos antigas (Django Signals)
- Filtro por nome com busca parcial
- Paginação (5 usuários por página)
- Interface responsiva com cards para mobile

### 4. Relatórios
- Relatório de usuários por departamento
- Opção "Todos os Departamentos"
- Interface responsiva
- Botão de impressão

## 🔧 Comandos Úteis

### Popular o banco de dados
```bash
python manage.py seed_database
```

### Criar novas migrations
```bash
python manage.py makemigrations
```

### Aplicar migrations
```bash
python manage.py migrate
```

### Acessar o shell do Django
```bash
python manage.py shell
```

### Acessar o banco de dados
```bash
python manage.py dbshell
```

### Criar superusuário (opcional)
```bash
python manage.py createsuperuser
```

## 🐛 Resolução de Problemas

### Erro: "relation does not exist"
**Causa:** Migrations não foram aplicadas
**Solução:**
```bash
python manage.py migrate
```

### Erro: "permission denied for schema public"
**Causa:** Usuário PostgreSQL sem permissões
**Solução:** Execute os comandos GRANT do Passo 4.2

### Erro: "ModuleNotFoundError"
**Causa:** Dependências não instaladas
**Solução:**
```bash
pip install -r requirements.txt
```

### Erro: "Could not connect to server"
**Causa:** PostgreSQL não está rodando
**Solução:**
```bash
# Windows (Services)
# Procure por "PostgreSQL" nos Serviços e inicie

# macOS
brew services start postgresql@17

# Linux
sudo systemctl start postgresql
```

### Fotos não aparecem
**Causa:** Seed não foi executado
**Solução:**
```bash
python manage.py seed_database
```

## 📚 Recursos Adicionais

### Django
- Documentação oficial: https://docs.djangoproject.com/
- Tutorial Django Girls: https://tutorial.djangogirls.org/

### PostgreSQL
- Documentação oficial: https://www.postgresql.org/docs/
- Tutorial W3Schools: https://www.w3schools.com/postgresql/

### Frontend
- Tailwind CSS: https://tailwindcss.com/docs
- Alpine.js: https://alpinejs.dev/
- HTMX: https://htmx.org/

## 👨‍💻 Desenvolvimento

### Ativar modo debug
No arquivo `.env`, certifique-se de que:
```env
DEBUG=True
```

### Desativar modo debug (produção)
```env
DEBUG=False
```
