# Análisis Estático de Código - PrevMora

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Herramientas Configuradas](#herramientas-configuradas)
3. [Backend (Python/FastAPI)](#backend-pythonfastapi)
4. [Frontend (Next.js/TypeScript)](#frontend-nextjstypescript)
5. [Análisis de Seguridad](#análisis-de-seguridad)
6. [Configuración y Uso](#configuración-y-uso)
7. [Integración Continua](#integración-continua)
8. [Métricas de Calidad](#métricas-de-calidad)
9. [Resolución de Problemas](#resolución-de-problemas)
10. [Referencias](#referencias)

## Introducción

El proyecto **PrevMora** implementa un conjunto completo de herramientas de análisis estático de código para garantizar la calidad, seguridad y mantenibilidad del software. Estas herramientas están configuradas en **modo estricto** siguiendo las mejores prácticas de la industria.

### Objetivos del Análisis Estático

- ✅ **Calidad de Código**: Detectar problemas de estilo y estructura
- ✅ **Seguridad**: Identificar vulnerabilidades potenciales
- ✅ **Mantenibilidad**: Asegurar código legible y bien documentado
- ✅ **Consistencia**: Enforcar estándares de nombramiento
- ✅ **Corrección Automática**: Formateo automático de código
- ✅ **Detección Temprana**: Identificar problemas antes del deploy

### Justificación de la Elección

Las herramientas seleccionadas se basan en:

1. **Estándares de la Industria**: Herramientas ampliamente adoptadas y reconocidas
2. **Integración Nativa**: Compatibilidad completa con Python y TypeScript
3. **Configurabilidad**: Capacidad de personalización según las necesidades del proyecto
4. **Automatización**: Soporte para corrección automática y integración en CI/CD
5. **Documentación**: Excelente documentación y soporte comunitario

## Herramientas Configuradas

### Resumen por Categoría

| Categoría | Backend (Python) | Frontend (TypeScript) |
|-----------|------------------|----------------------|
| **Formateo** | Black, isort | Prettier |
| **Linting** | Pylint, Flake8 | ESLint |
| **Tipos** | MyPy | TypeScript Compiler |
| **Seguridad** | Bandit, Safety | ESLint Security |
| **Documentación** | pydocstyle | ESLint JSDoc |
| **Código Muerto** | Vulture | ESLint |
| **Complejidad** | Pylint | ESLint Complexity |

### Puntuación de Herramientas

| Herramienta | Propósito | Configuración | Auto-fix | Nombrado |
|-------------|-----------|---------------|----------|----------|
| **Black** | Formateo Python | ✅ Estricta | ✅ Sí | N/A |
| **Pylint** | Linting Python | ✅ Estricta | ❌ No | ✅ Enforced |
| **MyPy** | Tipos Python | ✅ Estricta | ❌ No | N/A |
| **Bandit** | Seguridad Python | ✅ Estricta | ❌ No | N/A |
| **ESLint** | Linting TS/JS | ✅ Estricta | ✅ Parcial | ✅ Enforced |
| **Prettier** | Formateo TS/JS | ✅ Estricta | ✅ Sí | N/A |

## Backend (Python/FastAPI)

### 🎨 Black - Formateo de Código

**Propósito**: Formateo automático y consistente de código Python.

**Configuración** (`pyproject.toml`):
```toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
```

**Justificación**: Black es el estándar de facto para formateo Python, adoptado por proyectos como Django, Flask y FastAPI. Su filosofía de "opinionated formatter" elimina debates sobre estilo.

**Uso**:
```bash
# Formatear código
black app/ scripts/

# Verificar formato
black --check app/ scripts/
```

**Corrección Automática**: ✅ **Sí** - Formatea automáticamente el código

### 📑 isort - Organización de Imports

**Propósito**: Organización automática y consistente de imports Python.

**Configuración** (`pyproject.toml`):
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["app"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
```

**Justificación**: isort mantiene los imports organizados según PEP 8, mejorando la legibilidad y reduciendo conflictos de merge.

**Corrección Automática**: ✅ **Sí** - Organiza imports automáticamente

### 🔍 Pylint - Análisis de Calidad

**Propósito**: Análisis exhaustivo de calidad de código Python.

**Configuración Estricta**:
- **Puntuación mínima**: 8.0/10
- **Enforcing de nombrado**: Regex patterns estrictos
- **Límites de complejidad**: Métodos, clases y archivos
- **Convenciones PEP 8**: Totalmente enforced

**Estándares de Nombramiento Enforced**:
```toml
[tool.pylint.NAMING]
module-naming-style = "snake_case"
class-naming-style = "PascalCase"
function-naming-style = "snake_case"
method-naming-style = "snake_case"
variable-naming-style = "snake_case"
const-naming-style = "UPPER_CASE"
```

**Justificación**: Pylint es la herramienta más completa para análisis de calidad Python, oficial del ecosistema Python.

**Corrección Automática**: ❌ **No** - Solo detección

### 🏷️ MyPy - Verificación de Tipos

**Propósito**: Verificación estática de tipos Python.

**Configuración Estricta**:
```toml
[tool.mypy]
python_version = "3.9"
disallow_untyped_defs = true
disallow_incomplete_defs = true
strict_equality = true
warn_unreachable = true
```

**Justificación**: MyPy es el type checker oficial para Python, desarrollado por Guido van Rossum. Detecta errores de tipos antes de runtime.

**Corrección Automática**: ❌ **No** - Solo detección

### 🔒 Bandit - Análisis de Seguridad

**Propósito**: Detección de vulnerabilidades de seguridad en código Python.

**Configuración**:
```toml
[tool.bandit]
exclude_dirs = ["tests", "venv"]
severity = "medium"
```

**Vulnerabilidades Detectadas**:
- Hardcoded passwords
- SQL injection
- Shell injection
- Insecure random
- Assert statements
- Exec/eval usage

**Justificación**: Bandit es el estándar para análisis de seguridad en Python, desarrollado por OpenStack.

**Corrección Automática**: ❌ **No** - Solo detección

### 📚 pydocstyle - Convenciones de Docstrings

**Propósito**: Verificación de convenciones de documentación.

**Configuración**:
```toml
[tool.pydocstyle]
convention = "google"
match = "(?!test_).*\.py"
```

**Justificación**: Sigue las convenciones de Google para docstrings, adoptadas por FastAPI y otros proyectos principales.

### 🧟 Vulture - Detección de Código Muerto

**Propósito**: Identificación de código no utilizado.

**Configuración**:
```toml
[tool.vulture]
min_confidence = 60
sort_by_size = true
```

**Justificación**: Ayuda a mantener el código limpio eliminando funciones, variables y clases no utilizadas.

### 🛡️ Safety - Vulnerabilidades en Dependencias

**Propósito**: Verificación de vulnerabilidades conocidas en dependencias.

**Uso**:
```bash
safety check -r requirements.txt
```

**Justificación**: Essential para detectar vulnerabilidades en packages de terceros.

## Frontend (Next.js/TypeScript)

### 🎨 Prettier - Formateo de Código

**Propósito**: Formateo automático y consistente de código TypeScript/JavaScript.

**Configuración**:
- Integración con TailwindCSS
- Sort imports automático
- Configuración consistent con el backend

**Justificación**: Prettier es el estándar de la industria para formateo JavaScript/TypeScript, adoptado por Facebook, Airbnb y Microsoft.

**Corrección Automática**: ✅ **Sí** - Formatea automáticamente

### 🔍 ESLint - Análisis de Calidad

**Propósito**: Análisis exhaustivo de calidad de código TypeScript/JavaScript.

**Configuración Estricta**:
- **Max warnings**: 0 (modo estricto)
- **Complexity limit**: 15
- **Max params**: 5
- **Max lines**: 500

**Estándares de Nombramiento Enforced**:
```javascript
'@typescript-eslint/naming-convention': [
  'error',
  { selector: 'variableLike', format: ['camelCase'] },
  { selector: 'typeLike', format: ['PascalCase'] },
  { selector: 'functionLike', format: ['camelCase'] }
]
```

**Reglas de Seguridad**:
- No eval/exec
- No script URLs
- Secure random
- XSS prevention

**Justificación**: ESLint es el linter estándar para JavaScript/TypeScript, con excelente soporte para React y Next.js.

**Corrección Automática**: ✅ **Parcial** - Muchas reglas tienen auto-fix

### 🏷️ TypeScript Compiler - Verificación de Tipos

**Propósito**: Verificación estática de tipos TypeScript.

**Configuración Estricta**:
```json
{
  "strict": true,
  "noImplicitAny": true,
  "strictNullChecks": true,
  "noImplicitReturns": true
}
```

**Justificación**: TypeScript compiler oficial de Microsoft, garantiza type safety completa.

**Corrección Automática**: ❌ **No** - Solo detección

## Análisis de Seguridad

### 🔐 Herramientas de Seguridad Implementadas

1. **Bandit** (Python): Vulnerabilidades en código
2. **Safety** (Python): Vulnerabilidades en dependencias
3. **npm audit** (Frontend): Vulnerabilidades en packages
4. **ESLint Security**: Reglas de seguridad JavaScript
5. **Trivy** (CI/CD): Scanner de vulnerabilidades
6. **GitGuardian** (CI/CD): Detección de secretos

### 🛡️ Tipos de Vulnerabilidades Detectadas

#### Backend
- **Injection Attacks**: SQL, Command, LDAP injection
- **Cryptographic Issues**: Weak algorithms, hardcoded keys
- **Authentication**: Weak password policies, session issues
- **Authorization**: Privilege escalation, access control
- **Dependencies**: Known CVEs in packages

#### Frontend
- **XSS Prevention**: Script injection, unsafe innerHTML
- **CSRF Protection**: Cross-site request forgery
- **Data Exposure**: Sensitive data in localStorage
- **Dependencies**: Known vulnerabilities in npm packages
- **Build Security**: Secure bundling and compilation

## Configuración y Uso

### 🚀 Instalación Rápida

```bash
# Configuración completa del entorno
./scripts/setup-dev.sh

# Instalar pre-commit hooks
pre-commit install
```

### 📋 Comandos Principales

#### Backend
```bash
# Formateo completo
black app/ && isort app/

# Análisis completo
pylint app/ --fail-under=8.0
mypy app/
bandit -r app/
flake8 app/
pydocstyle app/
vulture app/
safety check -r requirements.txt
```

#### Frontend
```bash
# Formateo y linting
npm run format
npm run lint:fix

# Análisis completo
npm run analyze  # format:check + lint:strict + type-check
```

#### Proyecto Completo
```bash
# Formatear todo el proyecto
./scripts/format-all.sh

# Verificar todo el proyecto
./scripts/check-all.sh
```

### ⚙️ Configuración de Editor

#### VSCode (Recomendado)

El proyecto incluye configuración automática para VSCode:

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "python.formatting.provider": "black",
  "python.linting.pylintEnabled": true
}
```

#### Extensiones Requeridas
- Python
- Black Formatter
- Pylint
- ESLint
- Prettier
- TypeScript

### 🔄 Pre-commit Hooks

Los hooks automáticos ejecutan análisis estático en cada commit:

```yaml
repos:
  - repo: https://github.com/psf/black
  - repo: https://github.com/pycqa/isort
  - repo: https://github.com/pycqa/flake8
  - repo: https://github.com/PyCQA/bandit
  - repo: https://github.com/pre-commit/mirrors-eslint
  - repo: https://github.com/pre-commit/mirrors-prettier
```

## Integración Continua

### 🚀 GitHub Actions

El proyecto incluye workflows de CI/CD completos:

#### Static Analysis Workflow
- **Backend Analysis**: Formateo, linting, tipos, seguridad
- **Frontend Analysis**: Formateo, linting, tipos, build
- **Security Analysis**: Trivy, secrets detection
- **Code Quality**: SonarCloud integration

#### Configuración de Calidad Gates

```yaml
# Requisitos para merge
- Pylint score ≥ 8.0
- MyPy: 0 type errors
- ESLint: 0 warnings
- Security: 0 high vulnerabilities
- Tests: 100% pass rate
- Coverage: ≥ 80%
```

### 📊 SonarQube Integration

Configuración completa para análisis de calidad:

```properties
# sonar-project.properties
sonar.qualitygate.wait=true
sonar.coverage.exclusions=**/tests/**
sonar.maintainability.rating=A
sonar.security.rating=A
sonar.reliability.rating=A
```

**Métricas Monitoreadas**:
- **Maintainability**: Deuda técnica, code smells
- **Reliability**: Bugs, error-prone code
- **Security**: Vulnerabilidades, hotspots
- **Coverage**: Cobertura de tests
- **Duplications**: Código duplicado

## Métricas de Calidad

### 🎯 Objetivos de Calidad

| Métrica | Objetivo | Herramienta |
|---------|----------|-------------|
| **Pylint Score** | ≥ 8.0/10 | Pylint |
| **Type Coverage** | 100% | MyPy |
| **Security Issues** | 0 High | Bandit, Safety |
| **Code Complexity** | ≤ 15 | Pylint, ESLint |
| **Test Coverage** | ≥ 80% | pytest, jest |
| **Documentation** | ≥ 80% | pydocstyle |

### 📈 Monitoring Continuo

```bash
# Generar reporte de métricas
./scripts/quality-report.sh

# Métricas específicas
pylint app/ --output-format=json > pylint-report.json
mypy app/ --html-report mypy-report/
bandit -r app/ -f json -o bandit-report.json
```

### 🏆 Badges de Calidad

El proyecto puede incluir badges para mostrar métricas:

- [![Code Quality](https://sonarcloud.io/api/project_badges/measure?project=prevmora&metric=alert_status)](https://sonarcloud.io/dashboard?id=prevmora)
- [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=prevmora&metric=security_rating)](https://sonarcloud.io/dashboard?id=prevmora)
- [![Coverage](https://codecov.io/gh/prevmora/project/branch/main/graph/badge.svg)](https://codecov.io/gh/prevmora/project)

## Resolución de Problemas

### ❗ Problemas Comunes

#### Backend

**Error: Pylint score bajo**
```bash
# Ver errores específicos
pylint app/ --reports=y

# Deshabilitar regla específica (temporal)
# pylint: disable=C0103

# Corregir automáticamente lo posible
black app/ && isort app/
```

**Error: MyPy type errors**
```bash
# Ver detalles de errores
mypy app/ --show-error-codes

# Ignorar error específico (no recomendado)
# type: ignore[error-code]

# Agregar type hints
def function(param: str) -> int:
```

**Error: Bandit security issues**
```bash
# Ver detalles específicos
bandit -r app/ -ll

# Ignorar false positive (cuidadosamente)
# nosec B101
```

#### Frontend

**Error: ESLint warnings**
```bash
# Auto-fix cuando sea posible
npm run lint:fix

# Ver reglas específicas
npx eslint src/ --format=verbose

# Deshabilitar regla específica (temporal)
// eslint-disable-next-line rule-name
```

**Error: TypeScript errors**
```bash
# Ver errores detallados
npm run type-check

# Generar tipos para librería
npm install @types/library-name
```

### 🔧 Configuración Personalizada

#### Ajustar Severidad de Pylint
```toml
[tool.pylint]
fail-under = 7.5  # Reducir temporalmente
disable = ["C0114", "C0115"]  # Deshabilitar docstrings temporalmente
```

#### Ajustar Reglas de ESLint
```javascript
rules: {
  "complexity": ["warn", 20],  // Aumentar límite de complejidad
  "@typescript-eslint/no-explicit-any": "warn"  // Cambiar a warning
}
```

### 🚨 Modo de Emergencia

Si las herramientas bloquean desarrollo urgente:

```bash
# Deshabilitar pre-commit temporalmente
SKIP=pylint,bandit git commit -m "Emergency fix"

# Bypass de análisis estático (NO RECOMENDADO)
git commit --no-verify -m "Bypass hooks"
```

**⚠️ Importante**: Siempre corregir issues después del bypass.

## Referencias

### 📚 Documentación Oficial

#### Python Tools
- [Black Documentation](https://black.readthedocs.io/)
- [Pylint Documentation](https://pylint.pycqa.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [pydocstyle Documentation](http://www.pydocstyle.org/)

#### TypeScript/JavaScript Tools
- [ESLint Documentation](https://eslint.org/docs/)
- [Prettier Documentation](https://prettier.io/docs/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [@typescript-eslint Documentation](https://typescript-eslint.io/)

#### Security Tools
- [Safety Documentation](https://github.com/pyupio/safety)
- [npm audit Documentation](https://docs.npmjs.com/cli/v8/commands/npm-audit)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)

#### Quality Tools
- [SonarQube Documentation](https://docs.sonarqube.org/)
- [Pre-commit Documentation](https://pre-commit.com/)

### 🏛️ Estándares y Guías

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [TypeScript Style Guide](https://github.com/Microsoft/TypeScript/wiki/Coding-guidelines)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

### 🔗 Herramientas Adicionales

- [Codecov](https://codecov.io/) - Code coverage reports
- [FOSSA](https://fossa.com/) - License compliance
- [Snyk](https://snyk.io/) - Dependency vulnerability scanning
- [CodeClimate](https://codeclimate.com/) - Automated code review

---

**Documento creado**: Septiembre 2025  
**Última actualización**: Septiembre 2025  
**Versión**: 1.0  
**Mantenido por**: Equipo de desarrollo PrevMora

---

🎯 **El análisis estático es fundamental para mantener la calidad, seguridad y mantenibilidad del código. Estas herramientas están aquí para ayudarte a escribir mejor código, no para obstaculizar el desarrollo.**
