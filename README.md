# PrevMora

PrevMora is a microfinance-focused solution designed to help financial institutions manage early-stage credit collections. Project for the seventh-semester course "Integrative Project 2" (ST0258) taught at EAFIT University.

## 🏗️ Arquitectura del Proyecto

```
PrevMora/
├── backend/               # API Backend (FastAPI + Python)
│   └── credit_management/ # Microservicio principal
├── frontend/              # Aplicación Web (Next.js + TypeScript)
├── docs/                  # Documentación del proyecto
│   └── wiki/              # Wiki y estándares
└── README.md
```

## 🚀 Tecnologías

### Backend
- **FastAPI** - Framework web moderno para APIs
- **Python 3.9+** - Lenguaje de programación
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **Pytest** - Framework de testing

### Frontend
- **Next.js 15** - Framework React con SSR
- **TypeScript** - Superset tipado de JavaScript
- **TailwindCSS 4** - Framework CSS utilitario
- **DaisyUI** - Biblioteca de componentes
- **React 19** - Biblioteca para interfaces de usuario

### Base de Datos
- **SQL Server** - Base de datos principal

## 📋 Requisitos Previos

- **Node.js** 18+ y npm
- **Python** 3.9+
- **SQL Server** (local o remoto)
- **Git**

## 🛠️ Configuración de Desarrollo

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd PrevMora
```

### 2. Backend Setup
```bash
cd backend/credit_management

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu configuración

# Ejecutar migraciones
python scripts/recreate_database.py

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.local.example .env.local
# Editar .env.local con tu configuración

# Iniciar servidor de desarrollo
npm run dev
```

## 📖 Documentación

### 📚 Wiki del Proyecto
- **[Estándares de Nombramiento](docs/wiki/naming-standards.md)** - Convenciones de código y nomenclatura
- **[Análisis Estático de Código](docs/wiki/static-analysis.md)** - Herramientas de calidad y seguridad
- **[Configuración de Desarrollo](docs/wiki/development-setup.md)** - Herramientas y flujo de trabajo

### 🔧 Estándares de Desarrollo

Este proyecto sigue estándares de código estrictos para mantener la calidad y consistencia:

- **Backend**: [PEP 8](https://peps.python.org/pep-0008/) para Python
- **Frontend**: [Estándares de TypeScript](https://typescript-lang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
- **Base de Datos**: Convenciones SQL estándar

**📋 Lee nuestros [Estándares de Nombramiento](docs/wiki/naming-standards.md) antes de contribuir.**

## 🧪 Testing

### Backend
```bash
cd backend/credit_management
pytest
coverage run -m pytest && coverage report
```

### Frontend
```bash
cd frontend
npm test
npm run test:coverage
```

## 🚀 Producción

### Backend
```bash
cd backend/credit_management
docker-compose up -d
```

### Frontend
```bash
cd frontend
npm run build
npm start
```

## 📝 Scripts Útiles

### Formateo de Código
```bash
# Backend
cd backend/credit_management
black app/ && isort app/

# Frontend
cd frontend
npm run format
```

### Linting
```bash
# Backend
pylint app/

# Frontend
npm run lint
```

## 🤝 Contribución

1. Lee los [Estándares de Nombramiento](docs/wiki/naming-standards.md)
2. Configura las [Herramientas de Desarrollo](docs/wiki/development-setup.md)
3. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
4. Asegúrate de que el código pase todos los tests y linters
5. Realiza commit siguiendo [Conventional Commits](https://www.conventionalcommits.org/)
6. Envía un Pull Request

## 📄 Licencia

Este proyecto es desarrollado como parte del curso "Proyecto Integrador 2" (ST0258) en la Universidad EAFIT.

## 👥 Equipo de Desarrollo

- Proyecto académico - Universidad EAFIT
- Curso: ST0258 - Proyecto Integrador 2
- Semestre: 2025-1

---

⚡ **Nota**: Este es un proyecto educativo para la gestión de microfinanzas y cobranza temprana de créditos.
