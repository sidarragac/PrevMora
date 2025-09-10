#!/bin/bash

# Script de configuración inicial para desarrollo en PrevMora
# Configura el entorno de desarrollo con todas las herramientas necesarias

set -e  # Salir si algún comando falla

echo "🚀 Configurando entorno de desarrollo para PrevMora"
echo "===================================================="

# Verificar que estamos en el directorio correcto
if [[ ! -f "README.md" ]] || [[ ! -d "backend" ]] || [[ ! -d "frontend" ]]; then
    echo "❌ Error: Ejecuta este script desde la raíz del proyecto PrevMora"
    exit 1
fi

# Verificar herramientas requeridas
echo ""
echo "🔍 Verificando herramientas requeridas..."

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
    echo "✅ Python $PYTHON_VERSION encontrado"
else
    echo "❌ Python 3.9+ es requerido. Por favor, instálalo primero."
    exit 1
fi

# Verificar Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js $NODE_VERSION encontrado"
else
    echo "❌ Node.js 18+ es requerido. Por favor, instálalo primero."
    exit 1
fi

# Verificar npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✅ npm $NPM_VERSION encontrado"
else
    echo "❌ npm es requerido. Por favor, instálalo primero."
    exit 1
fi

# Configurar Backend
echo ""
echo "📦 Configurando backend (Python/FastAPI)..."
echo "---------------------------------------------"

if [[ -d "backend/credit_management" ]]; then
    cd backend/credit_management
    
    # Crear entorno virtual si no existe
    if [[ ! -d "venv" ]]; then
        echo "🔧 Creando entorno virtual..."
        python3 -m venv venv
    else
        echo "✅ Entorno virtual ya existe"
    fi
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Actualizar pip
    echo "📥 Actualizando pip..."
    pip install --upgrade pip --quiet
    
    # Instalar dependencias del proyecto
    if [[ -f "requirements.txt" ]]; then
        echo "📦 Instalando dependencias del proyecto..."
        pip install -r requirements.txt --quiet
    fi
    
    # Instalar herramientas de desarrollo
    echo "🛠️  Instalando herramientas de desarrollo..."
    pip install black isort pylint mypy pytest coverage pre-commit --quiet
    
    echo "✅ Backend configurado correctamente"
    
    cd ../..
else
    echo "⚠️  Directorio backend/credit_management no encontrado"
fi

# Configurar Frontend
echo ""
echo "🌐 Configurando frontend (Next.js/TypeScript)..."
echo "------------------------------------------------"

if [[ -d "frontend" ]]; then
    cd frontend
    
    # Instalar dependencias
    echo "📦 Instalando dependencias..."
    npm install --silent
    
    echo "✅ Frontend configurado correctamente"
    
    cd ..
else
    echo "⚠️  Directorio frontend no encontrado"
fi

# Configurar Git hooks (opcional)
echo ""
echo "🔗 Configurando Git hooks..."
echo "----------------------------"

if command -v git &> /dev/null && [[ -d ".git" ]]; then
    # Configurar pre-commit si está disponible
    if command -v pre-commit &> /dev/null; then
        echo "🎣 Configurando pre-commit hooks..."
        
        # Crear configuración básica de pre-commit
        if [[ ! -f ".pre-commit-config.yaml" ]]; then
            cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        files: ^backend/
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        files: ^backend/

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
      - id: prettier
        files: ^frontend/
        exclude: ^frontend/node_modules/
EOF
            echo "📝 Archivo .pre-commit-config.yaml creado"
        fi
        
        # Instalar hooks
        pre-commit install
        echo "✅ Pre-commit hooks instalados"
    else
        echo "⚠️  pre-commit no está disponible. Instálalo con: pip install pre-commit"
    fi
else
    echo "⚠️  No es un repositorio Git o Git no está disponible"
fi

# Crear archivos de configuración del editor
echo ""
echo "⚙️  Configurando editor (VSCode)..."
echo "-----------------------------------"

mkdir -p .vscode

# Configuración de VSCode
if [[ ! -f ".vscode/settings.json" ]]; then
    cat > .vscode/settings.json << 'EOF'
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
  "python.sortImports.provider": "isort",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
EOF
    echo "📝 Configuración de VSCode creada"
fi

# Extensiones recomendadas
if [[ ! -f ".vscode/extensions.json" ]]; then
    cat > .vscode/extensions.json << 'EOF'
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.isort",
    "bradlc.vscode-tailwindcss",
    "ms-python.pylint"
  ]
}
EOF
    echo "📝 Extensiones recomendadas de VSCode configuradas"
fi

# Resumen final
echo ""
echo "🎉 ¡Configuración completada exitosamente!"
echo "=========================================="
echo ""
echo "📋 Tu entorno de desarrollo está listo:"
echo "  ✅ Backend configurado con Python y FastAPI"
echo "  ✅ Frontend configurado con Next.js y TypeScript"
echo "  ✅ Herramientas de formateo y linting instaladas"
echo "  ✅ Scripts de utilidad disponibles"
echo "  ✅ Configuración de editor creada"
echo ""
echo "🚀 Próximos pasos:"
echo "  1. Lee la documentación: docs/wiki/naming-standards.md"
echo "  2. Configura variables de entorno (.env)"
echo "  3. Ejecuta tests: ./scripts/check-all.sh"
echo "  4. Formatea código: ./scripts/format-all.sh"
echo ""
echo "📖 Documentación adicional:"
echo "  - README principal: README.md"
echo "  - Wiki del proyecto: docs/wiki/README.md"
echo "  - Configuración de desarrollo: docs/wiki/development-setup.md"
echo ""
echo "¡Feliz desarrollo! 🎯"
