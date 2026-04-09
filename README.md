# Cell Project - ERP for Cell Church Management

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.0-green)
![Angular](https://img.shields.io/badge/angular-frontend-red)

**Cell Project** is an ERP system developed for managing churches organized under the cell model. The initial focus is on the Youth Ministry (Mag) administration, with architecture prepared for future expansion to other church areas.

> **⚠️ Current Phase:** The project is in its **early days of development**. Backend structuring, data modeling, and environment setup are currently in progress.

---

## 👥 Team

| Name | Role | Primary Stack |
|------|------|---------------|
| **Lucas Oliveira** | Backend Developer | Django, DRF, PostgreSQL |
| **Leandro Finochio** | Frontend Developer | Angular, TypeScript |
| **Guilherme Gomes** | Data Analyst | Python, Pandas, Jupyter, PowerBI |

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 5.0 + Django REST Framework
- **Database:** PostgreSQL (via `psycopg2-binary`)
- **Authentication:** JWT (Simple JWT)
- **Data Validation:** Pydantic
- **Dependency Management:** Poetry 2.0

### Frontend
- **Framework:** Angular
- **Communication:** HTTP Client for REST API consumption

### Data Analysis
- **Libraries:** Pandas, NumPy
- **Visualization:** To be defined (Matplotlib/Seaborn/Power BI)

### Development Tools
- **Documentation:** MkDocs + Material + **Qwen CLI** (docs and testing assistance)
- **Testing:** Pytest + Pytest-Django + **Qwen CLI**
- **Linting/Formatting:** Ruff
- **AI Integration:** OpenAI API

---

## 📦 Core Dependencies

### Production
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

### Development
```
ruff>=0.12.7
taskipy>=1.14.1
pytest-django>=4.8.0
pytest-cov>=5.0
flake8>=7.0.0
pandas>=2.0.0
```

---

## 🚀 Installation and Setup (Development Environment)

### Prerequisites
- Python 3.13
- Poetry 2.0+
- PostgreSQL 14+
- Node.js 18+ (for Angular frontend)
- Git

### Backend Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cell_project
   ```

2. **Configure Python environment with Poetry**
   ```bash
   poetry env use 3.13
   poetry install
   ```

3. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```ini
   # Django
   SECRET_KEY=your-super-secure-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database
   DATABASE_URL=postgresql://user:password@localhost:5432/cell_db
   DB_NAME=cell_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # OpenAI (for AI features)
   OPENAI_API_KEY=your-openai-key
   
   # JWT
   JWT_SECRET_KEY=your-jwt-key
   ```

5. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE cell_db;
   ```

6. **Run initial migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a Django superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```
   
   The API will be available at: `http://localhost:8000/api/`

---

## 🖥️ Angular Frontend (Development)

### Initial Setup

1. **Navigate to the frontend folder**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   
   Create the file `src/environments/environment.ts`:
   ```typescript
   export const environment = {
     production: false,
     apiUrl: 'http://localhost:8000/api'
   };
   ```

4. **Start Angular development server**
   ```bash
   ng serve
   ```
   
   The application will be available at: `http://localhost:4200/`

---

## 📊 Data Analysis with Pandas

Data analysis scripts are located in the `analytics/` folder.

### Usage example:
```python
import pandas as pd
from django_pandas.io import read_frame

# Export attendance data for analysis
from cell_project.members.models import MonthlyAttendance

qs = MonthlyAttendance.objects.filter(reference_month__year=2026)
df = read_frame(qs)

# Analysis with Pandas
average_attendance = df.groupby('cell_id')['percentage'].mean()
```

### Jupyter Notebooks
To run interactive analyses:
```bash
poetry run jupyter notebook
```

---

## 🤖 Qwen CLI - Documentation and Testing Assistant

**Qwen CLI** accelerates development through:

- Automatic docstring generation
- Test case suggestions
- Documentation review
- Unit test writing assistance

### Useful commands:

```bash
# Generate docstring for a function
qwen docstring "def calculate_attendance(month, attendances):"

# Suggest tests for a Django model
qwen suggest-tests "class Cell(models.Model):"

# Review MkDocs documentation
qwen review-docs docs/
```

> **Note:** Ensure Qwen CLI is installed and configured with your API key.

---

## 📋 Quick Commands (Taskipy)

| Command | Description |
|---------|-------------|
| `poetry run task lint` | Run code checks with Ruff |
| `poetry run task format` | Auto-format code |
| `poetry run task test` | Run test suite with coverage |
| `poetry run task docs` | Start MkDocs server at `127.0.0.1:8001` |

---

## 📁 Project Structure (Overview)

```
cell_project/
├── backend/                    # Django project
│   ├── cell_project/          # Main settings
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   └── urls.py
│   ├── apps/                   # Modular Django applications
│   │   ├── core/              # Shared functionalities
│   │   ├── members/           # Member and person management
│   │   ├── cells/             # Cell management
│   │   ├── hierarchy/         # Leadership structure
│   │   ├── ministries/        # Ministries
│   │   ├── attendance/        # Attendance tracking
│   │   └── calendar/          # Annual calendar
│   ├── manage.py
│   └── requirements.txt       # Exported via Poetry
│
├── frontend/                   # Angular application
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
├── analytics/                  # Data analysis scripts
│   ├── notebooks/             # Jupyter notebooks
│   ├── scripts/               # Python scripts with Pandas
│   └── reports/               # Generated reports
│
├── docs/                       # MkDocs documentation
│   ├── docs/
│   │   ├── api/
│   │   ├── models/
│   │   └── guides/
│   └── mkdocs.yml
│
├── scripts/                    # Utility scripts
│   ├── backup_db.py
│   └── seed_data.py
│
├── tests/                      # Integration and E2E tests
│   ├── integration/
│   └── e2e/
│
├── .env.example               # Environment variables template
├── .gitignore
├── pyproject.toml             # Poetry configuration
├── poetry.lock                # Poetry lock file
├── README.md                  # This file
└── LICENSE
```

---

## 🧪 Testing

### Run all tests
```bash
poetry run task test
```

### Run specific tests
```bash
poetry run pytest apps/members/tests/
```

### Generate HTML coverage report
```bash
poetry run pytest --cov=cell_project --cov-report=html
# Open htmlcov/index.html in your browser
```

---

## 📈 Development Roadmap

| Phase | Task | Status |
|-------|------|--------|
| **1 - Foundation** | Poetry and Django environment setup | ✅ Completed |
| **1 - Foundation** | Tech stack definition | ✅ Completed |
| **1 - Foundation** | Data modeling | 🔄 In Progress |
| **2 - Frontend Base** | Base template creation | ⏳ Pending |
| **2 - Frontend Base** | Components creation | ⏳ Pending |
| **2 - Frontend Base** | Domain layer validation | ⏳ Pending |
| **3 - Admin & CRUD** | Domain admin creation | ⏳ Pending |
| **3 - Admin & CRUD** | CRUD: Read - Domain list | ⏳ Pending |
| **3 - Admin & CRUD** | Domain filters | ⏳ Pending |
| **3 - Admin & CRUD** | CRUD: Create - Domain creation | ⏳ Pending |
| **3 - Admin & CRUD** | Domain forms styling | ⏳ Pending |
| **3 - Admin & CRUD** | CRUD: Read - Domain details | ⏳ Pending |
| **3 - Admin & CRUD** | Domain action menu | ⏳ Pending |
| **3 - Admin & CRUD** | CRUD: Update - Domain update | ⏳ Pending |
| **3 - Admin & CRUD** | CRUD: Delete - Domain deletion | ⏳ Pending |
| **3 - Admin & CRUD** | Pagination implementation | ⏳ Pending |
| **4 - Authentication** | Login route creation | ⏳ Pending |
| **4 - Authentication** | Login screen creation | ⏳ Pending |
| **4 - Authentication** | User authentication implementation | ⏳ Pending |
| **4 - Authentication** | Logout implementation | ⏳ Pending |
| **4 - Authentication** | User permissions | ⏳ Pending |
| **4 - Authentication** | User groups and permissions | ⏳ Pending |
| **4 - Authentication** | Dynamic interface based on permissions | ⏳ Pending |
| **5 - API** | Domain API creation | ⏳ Pending |
| **5 - API** | JWT API authentication | ⏳ Pending |
| **5 - API** | API authentication and permissions | ⏳ Pending |
| **6 - Final** | Final adjustments and best practices | ⏳ Pending |

**Legend:** ✅ Completed | 🔄 In Progress | ⏳ Pending

---

## 🤝 Contributing

### Git Workflow

1. **Always create a branch from `develop`**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/feature-name
   ```

2. **Commit convention (Conventional Commits)**
   ```
   feat: add Cell model
   fix: correct attendance calculation
   docs: update README
   test: add tests for Members
   refactor: reorganize folder structure
   ```

3. **Before opening a Pull Request**
   ```bash
   poetry run task lint
   poetry run task format
   poetry run task test
   ```

---

## 📝 Development Notes

### For Backend Team (Lucas)
- Keep `poetry.lock` versioned
- Update `requirements.txt` before deployments:
  ```bash
  poetry export -f requirements.txt --output requirements.txt --without-hashes
  ```

### For Frontend Team (Leandro)
- Consume API at `http://localhost:8000/api/`
- Interactive documentation available at `http://localhost:8000/api/docs/`

### For Data Analysis (Guilherme)
- Data exportable via Django REST Framework or direct SQL
- Jupyter notebooks in `analytics/notebooks/`
- Shared environment via Poetry (include `pandas` in dev group)

---

## 📄 License

This project is under the MIT License. See the `LICENSE` file for more details.

---

## 📞 Contact

| Role | Name | Email |
|------|------|-------|
| Backend Lead | Lucas Oliveira | lucas.oliveira.profissional@hotmail.com |
| Frontend Lead | Leandro Finochio | - |
| Data Lead | Guilherme Gomes | - |
