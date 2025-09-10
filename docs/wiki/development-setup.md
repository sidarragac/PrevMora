# Configuración de Desarrollo - PrevMora

## Herramientas de Formato y Linting

Este documento explica cómo configurar y usar las herramientas para mantener automáticamente los estándares de nombramiento y estilo del proyecto.

## Backend (Python/FastAPI)

### Herramientas Requeridas

Instala las herramientas de desarrollo:

```bash
cd backend/credit_management
pip install black isort pylint mypy pytest coverage
```

### Comandos Útiles

#### Formateo Automático
```bash
# Formatear código con Black
black app/ scripts/

# Ordenar imports con isort
isort app/ scripts/

# Formatear todo de una vez
black app/ scripts/ && isort app/ scripts/
```

#### Linting y Validación
```bash
# Verificar estilo con pylint
pylint app/

# Verificar tipos con mypy
mypy app/

# Ejecutar tests
pytest

# Generar reporte de cobertura
coverage run -m pytest && coverage report
```

#### Pre-commit (Recomendado)
Configura pre-commit hooks para formatear automáticamente antes de cada commit:

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar hooks
pre-commit install
```

Crea `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/pylint
    rev: v2.17.4
    hooks:
      - id: pylint
```

## Frontend (Next.js/TypeScript)

### Herramientas Configuradas

El proyecto ya incluye:
- **ESLint**: Linting de código
- **Prettier**: Formateo automático
- **TypeScript**: Verificación de tipos

### Comandos Útiles

```bash
cd frontend

# Formatear código
npm run format

# Verificar linting
npm run lint

# Verificar linting y corregir automáticamente
npm run lint -- --fix

# Verificar tipos TypeScript
npx tsc --noEmit
```

### Configuración del Editor

#### VSCode (Recomendado)

Crea `.vscode/settings.json` en la raíz del proyecto:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "python.defaultInterpreterPath": "./backend/credit_management/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.sortImports.provider": "isort"
}
```

Extensiones recomendadas (`.vscode/extensions.json`):
```json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.isort",
    "bradlc.vscode-tailwindcss"
  ]
}
```

## Flujo de Trabajo Recomendado

### 1. Antes de Desarrollar
```bash
# Backend
cd backend/credit_management
black app/ && isort app/

# Frontend
cd frontend
npm run format
```

### 2. Durante el Desarrollo
- Configura tu editor para formatear al guardar
- Ejecuta linting periódicamente
- Verifica tipos antes de commits importantes

### 3. Antes de Commits
```bash
# Backend
pylint app/ && mypy app/ && pytest

# Frontend
npm run lint && npx tsc --noEmit && npm test
```

### 4. Integración Continua
Agrega estos comandos a tu pipeline de CI/CD:

```yaml
# Ejemplo para GitHub Actions
- name: Backend Linting
  run: |
    cd backend/credit_management
    pip install -r requirements.txt
    pip install black isort pylint mypy
    black --check app/
    isort --check app/
    pylint app/
    mypy app/

- name: Frontend Linting
  run: |
    cd frontend
    npm install
    npm run lint
    npx tsc --noEmit
```

## Resolución de Problemas Comunes

### Backend

#### Error: "Module not found"
```bash
# Asegúrate de estar en el directorio correcto
cd backend/credit_management

# Activa el entorno virtual
source venv/bin/activate

# Reinstala dependencias
pip install -r requirements.txt
```

#### Conflictos entre Black e isort
```bash
# Usa el perfil de isort compatible con Black
isort --profile black app/
```

### Frontend

#### Error de ESLint con archivos nuevos
```bash
# Reinicia el servidor de ESLint en VSCode
# Cmd/Ctrl + Shift + P -> "ESLint: Restart ESLint Server"

# O ejecuta manualmente
npx eslint src/ --fix
```

#### Conflictos entre Prettier y ESLint
```bash
# Verifica que prettier esté configurado correctamente
npm run format
npm run lint -- --fix
```

## Scripts Utilitarios

### Script de Formateo Completo

Crea `scripts/format-all.sh`:
```bash
#!/bin/bash

echo "🔧 Formateando proyecto completo..."

# Backend
echo "📦 Formateando backend..."
cd backend/credit_management
black app/ scripts/
isort app/ scripts/

# Frontend
echo "🌐 Formateando frontend..."
cd ../../frontend
npm run format

echo "✅ Formateo completado!"
```

### Script de Verificación

Crea `scripts/check-all.sh`:
```bash
#!/bin/bash

echo "🔍 Verificando estándares del proyecto..."

# Backend
echo "📦 Verificando backend..."
cd backend/credit_management
pylint app/ || exit 1
mypy app/ || exit 1

# Frontend
echo "🌐 Verificando frontend..."
cd ../../frontend
npm run lint || exit 1
npx tsc --noEmit || exit 1

echo "✅ Verificación completada sin errores!"
```

---

**Mantener los estándares es responsabilidad de todo el equipo. Estas herramientas están aquí para ayudarte!** 🚀
