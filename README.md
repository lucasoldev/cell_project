# Cell Project - ERP para Gestão de Igreja em Células

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![Angular](https://img.shields.io/badge/angular-frontend-red)

**Cell Project** é um sistema ERP desenvolvido para a gestão de igrejas organizadas no modelo de células. O foco inicial está na administração do Ministério de Jovens (Mag), com arquitetura preparada para expansão futura para as demais áreas da igreja.

> **⚠️ Fase Atual:** O projeto encontra-se nos **primeiros dias de desenvolvimento**. Estruturação do backend, modelagem de dados e configuração do ambiente.

---

## 👥 Equipe

| Nome | Função | Stack Principal |
|------|--------|-----------------|
| **Lucas Oliveira** | Backend Developer | Django, DRF, PostgreSQL |
| **Leandro Finochio** | Frontend Developer | Angular, TypeScript |
| **Guilherme Gomes** | Data Analyst | Python, Pandas, Jupyter, PowerBI |

---

## 🛠️ Stack Tecnológica

### Backend
- **Framework:** Django 5.0 + Django REST Framework
- **Banco de Dados:** PostgreSQL (via `psycopg2-binary`)
- **Autenticação:** JWT (Simple JWT)
- **Validação de Dados:** Pydantic
- **Gerenciamento de Dependências:** Poetry 2.0

### Frontend
- **Framework:** Angular
- **Comunicação:** HTTP Client para consumo da API REST

### Análise de Dados
- **Bibliotecas:** Pandas, NumPy
- **Visualização:** A definir (Matplotlib/Seaborn/Power BI)

### Ferramentas de Desenvolvimento
- **Documentação:** MkDocs + Material + **Qwen CLI** (auxílio em docs e testes)
- **Testes:** Pytest + Pytest-Django + **Qwen CLI**
- **Linting/Formatação:** Ruff
- **Integração IA:** OpenAI API

---

## 📦 Dependências Principais

### Produção
```
django>=5.0.1
djangorestframework>=3.15.1
djangorestframework-simplejwt>=5.3.1
psycopg2-binary>=2.9.10
python-dotenv>=1.1.1
openai>=1.97.0
pydantic>=2.10.6
pyjwt>=2.10.1
mkdocs>=1.6.1
mkdocs-material>=9.6.20
```

### Desenvolvimento
```
ruff>=0.12.7
taskipy>=1.14.1
pytest-django>=4.8.0
pytest-cov>=5.0
flake8>=7.0.0
pandas>=2.0.0
```

---

## 🚀 Instalação e Configuração (Ambiente de Desenvolvimento)

### Pré-requisitos
- Python 3.13
- Poetry 2.0+
- PostgreSQL 14+
- Node.js 18+ (para frontend Angular)
- Git

### Passos para o Backend

1.  **Clone o repositório**
    ```bash
    git clone <url-do-repositorio>
    cd cell_project
    ```

2.  **Configure o ambiente Python com Poetry**
    ```bash
    poetry env use 3.13
    poetry install
    ```

3.  **Ative o ambiente virtual**
    ```bash
    poetry shell
    ```

4.  **Configure as variáveis de ambiente**
    
    Crie um arquivo `.env` na raiz do projeto:
    ```ini
    # Django
    SECRET_KEY=sua-chave-secreta-super-segura-aqui
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    
    # Database
    DATABASE_URL=postgresql://usuario:senha@localhost:5432/cell_db
    DB_NAME=cell_db
    DB_USER=postgres
    DB_PASSWORD=sua_senha
    DB_HOST=localhost
    DB_PORT=5432
    
    # OpenAI (para funcionalidades de IA)
    OPENAI_API_KEY=sua-chave-openai
    
    # JWT
    JWT_SECRET_KEY=sua-chave-jwt
    ```

5.  **Crie o banco de dados PostgreSQL**
    ```sql
    CREATE DATABASE cell_db;
    ```

6.  **Execute as migrações iniciais**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7.  **Crie um superusuário Django**
    ```bash
    python manage.py createsuperuser
    ```

8.  **Inicie o servidor de desenvolvimento**
    ```bash
    python manage.py runserver
    ```
    
    A API estará disponível em: `http://localhost:8000/api/`

---

## 🖥️ Frontend Angular (Desenvolvimento)

### Configuração Inicial

1.  **Acesse a pasta do frontend**
    ```bash
    cd frontend
    ```

2.  **Instale as dependências**
    ```bash
    npm install
    ```

3.  **Configure o ambiente**
    
    Crie o arquivo `src/environments/environment.ts`:
    ```typescript
    export const environment = {
      production: false,
      apiUrl: 'http://localhost:8000/api'
    };
    ```

4.  **Inicie o servidor de desenvolvimento Angular**
    ```bash
    ng serve
    ```
    
    A aplicação estará disponível em: `http://localhost:4200/`

---

## 📊 Análise de Dados com Pandas

Os scripts de análise de dados estão localizados na pasta `analytics/`.

### Exemplo de uso:
```python
import pandas as pd
from django_pandas.io import read_frame

# Exportar dados de assiduidade para análise
from cell_project.members.models import AssiduidadeMensal

qs = AssiduidadeMensal.objects.filter(mes_referencia__year=2026)
df = read_frame(qs)

# Análise com Pandas
media_assiduidade = df.groupby('celula_id')['percentual'].mean()
```

### Notebooks Jupyter
Para executar análises interativas:
```bash
poetry run jupyter notebook
```

---

## 🤖 Qwen CLI - Auxiliar de Documentação e Testes

O **Qwen CLI** é utilizado para acelerar o desenvolvimento através de:

- Geração automática de docstrings
- Sugestão de casos de teste
- Revisão de documentação
- Auxílio na escrita de testes unitários

### Comandos úteis:

```bash
# Gerar docstring para uma função
qwen docstring "def calcular_assiduidade(mes, presencas):"

# Sugerir testes para um modelo Django
qwen suggest-tests "class Celula(models.Model):"

# Revisar documentação MkDocs
qwen review-docs docs/
```

> **Nota:** Certifique-se de ter o Qwen CLI instalado e configurado com sua chave API.

---

## 📋 Comandos Rápidos (Taskipy)

| Comando | Descrição |
|---------|-----------|
| `poetry run task lint` | Executa verificação de código com Ruff |
| `poetry run task format` | Formata o código automaticamente |
| `poetry run task test` | Executa a suite de testes com cobertura |
| `poetry run task docs` | Inicia o servidor MkDocs em `127.0.0.1:8001` |

---

## 📁 Estrutura do Projeto (Visão Geral)

```
cell_project/
├── backend/                    # Projeto Django
│   ├── cell_project/          # Configurações principais
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   └── urls.py
│   ├── apps/                   # Aplicações Django modulares
│   │   ├── core/              # Funcionalidades compartilhadas
│   │   ├── members/           # Gestão de membros e pessoas
│   │   ├── cells/             # Gestão de células
│   │   ├── hierarchy/         # Estrutura de liderança
│   │   ├── ministries/        # Ministérios
│   │   ├── attendance/        # Frequência e assiduidade
│   │   └── calendar/          # Calendário anual
│   ├── manage.py
│   └── requirements.txt       # Exportado via Poetry
│
├── frontend/                   # Aplicação Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── modules/
│   │   │   │   ├── members/
│   │   │   │   ├── cells/
│   │   │   │   └── reports/
│   │   │   └── shared/
│   │   └── environments/
│   ├── angular.json
│   └── package.json
│
├── analytics/                  # Scripts de análise de dados
│   ├── notebooks/             # Jupyter notebooks
│   ├── scripts/               # Scripts Python com Pandas
│   └── reports/               # Relatórios gerados
│
├── docs/                       # Documentação MkDocs
│   ├── docs/
│   │   ├── api/
│   │   ├── models/
│   │   └── guides/
│   └── mkdocs.yml
│
├── scripts/                    # Scripts utilitários
│   ├── backup_db.py
│   └── seed_data.py
│
├── tests/                      # Testes de integração e E2E
│   ├── integration/
│   └── e2e/
│
├── .env.example               # Template de variáveis de ambiente
├── .gitignore
├── pyproject.toml             # Configuração Poetry
├── poetry.lock                # Lock file do Poetry
├── README.md                  # Este arquivo
└── LICENSE
```

---

## 🧪 Testes

### Executar todos os testes
```bash
poetry run task test
```

### Executar testes específicos
```bash
poetry run pytest apps/members/tests/
```

### Gerar relatório de cobertura HTML
```bash
poetry run pytest --cov=cell_project --cov-report=html
# Abra htmlcov/index.html no navegador
```

---

### Roadmap de Desenvolvimento

| Fase | Tarefa | Status |
|------|--------|--------|
| **1 - Fundação** | Configuração do ambiente Poetry e Django | ✅ Concluído |
| **1 - Fundação** | Definição da stack tecnológica | ✅ Concluído |
| **1 - Fundação** | Implementar modelos (Models) principais | 🔄 Em andamento |
| **1 - Fundação** | Configurar Django Admin | ⏳ Pendente |
| **2 - Core** | Implementar autenticação JWT | ⏳ Pendente |
| **2 - Core** | Criar endpoints REST CRUD | ⏳ Pendente |
| **2 - Core** | Estrutura de hierarquia de liderança | ⏳ Pendente |
| **3 - Funcionalidades** | Sistema de frequência e assiduidade | ⏳ Pendente |
| **3 - Funcionalidades** | Gestão de calendário anual | ⏳ Pendente |
| **3 - Funcionalidades** | Relatórios com Pandas | ⏳ Pendente |
| **4 - Frontend** | Setup do projeto Angular | ⏳ Pendente |
| **4 - Frontend** | Tela de login | ⏳ Pendente |
| **4 - Frontend** | Dashboard básico | ⏳ Pendente |
| **5 - Expansão** | Integração com OpenAI | ⏳ Pendente |
| **5 - Expansão** | Módulo de ministérios | ⏳ Pendente |
| **5 - Expansão** | Expansão para áreas adultas | ⏳ Pendente |

---

## 🤝 Contribuindo

### Fluxo de Trabalho com Git

1. **Sempre crie uma branch a partir de `develop`**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/nome-da-feature
   ```

2. **Padrão de commits (Conventional Commits)**
   ```
   feat: adiciona modelo de Célula
   fix: corrige cálculo de assiduidade
   docs: atualiza README
   test: adiciona testes para Membros
   refactor: reorganiza estrutura de pastas
   ```

3. **Antes de abrir um Pull Request**
   ```bash
   poetry run task lint
   poetry run task format
   poetry run task test
   ```

---

## 📝 Notas de Desenvolvimento

### Para o Time de Backend (Lucas)
- Manter o `poetry.lock` versionado
- Atualizar `requirements.txt` antes de deploys:
  ```bash
  poetry export -f requirements.txt --output requirements.txt --without-hashes
  ```

### Para o Time de Frontend (Leandro)
- Consumir a API em `http://localhost:8000/api/`
- Documentação interativa disponível em `http://localhost:8000/api/docs/`

### Para Análise de Dados (Guilherme)
- Dados exportáveis via Django REST Framework ou direct SQL
- Notebooks Jupyter na pasta `analytics/notebooks/`
- Ambiente compartilhado via Poetry (incluir `pandas` no grupo dev)

---

## 📞 Contato

| Função | Nome | Email |
|--------|------|-------|
| Backend Lead | Lucas Oliveira | lucas.oliveira.profissional@hotmail.com |
| Frontend Lead | Leandro Finochio | - |
| Data Lead | Guilherme Gomes | - |
