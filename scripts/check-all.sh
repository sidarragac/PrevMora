#!/bin/bash

# Script para verificar estándares de código del proyecto PrevMora
# Ejecuta linters y verificaciones de tipo en backend y frontend

set -e  # Salir si algún comando falla

echo "🔍 Verificando estándares del proyecto PrevMora..."
echo "================================================"

# Variables para tracking de errores
BACKEND_ERRORS=0
FRONTEND_ERRORS=0

# Verificar que estamos en el directorio correcto
if [[ ! -f "README.md" ]] || [[ ! -d "backend" ]] || [[ ! -d "frontend" ]]; then
    echo "❌ Error: Ejecuta este script desde la raíz del proyecto PrevMora"
    exit 1
fi

# Backend - Python/FastAPI
echo ""
echo "📦 Verificando backend (Python/FastAPI)..."
echo "--------------------------------------------"

if [[ -d "backend/credit_management" ]]; then
    cd backend/credit_management
    
    # Activar entorno virtual
    if [[ -d "venv" ]]; then
        source venv/bin/activate
    else
        echo "❌ Error: No se encontró entorno virtual en backend/credit_management/venv"
        BACKEND_ERRORS=1
    fi
    
    if [[ $BACKEND_ERRORS -eq 0 ]]; then
        # Verificar instalación de herramientas
        echo "📥 Verificando herramientas de análisis estático..."
        pip install pylint mypy pytest black isort flake8 bandit pydocstyle vulture safety --quiet
        
        echo "🎨 Verificando formato con Black..."
        if black --check app/ scripts/ --quiet; then
            echo "✅ Black: Código correctamente formateado"
        else
            echo "❌ Black: Código necesita formateo"
            BACKEND_ERRORS=1
        fi
        
        echo ""
        echo "📑 Verificando imports con isort..."
        if isort --check-only app/ scripts/ --quiet; then
            echo "✅ isort: Imports correctamente organizados"
        else
            echo "❌ isort: Imports necesitan reorganización"
            BACKEND_ERRORS=1
        fi
        
        echo ""
        echo "🔍 Ejecutando Flake8..."
        if flake8 app/ scripts/; then
            echo "✅ Flake8: Sin errores de estilo"
        else
            echo "❌ Flake8: Errores de estilo encontrados"
            BACKEND_ERRORS=1
        fi
        
        echo ""
        echo "🔍 Ejecutando PyLint..."
        if pylint app/ scripts/ --fail-under=8.0; then
            echo "✅ PyLint: Calidad de código satisfactoria (≥8.0)"
        else
            echo "❌ PyLint: Calidad de código insuficiente (<8.0)"
            BACKEND_ERRORS=1
        fi
        
        echo ""
        echo "🏷️ Verificando tipos con MyPy..."
        if mypy app/ --no-error-summary; then
            echo "✅ MyPy: Sin errores de tipos"
        else
            echo "❌ MyPy: Errores de tipos encontrados"
            BACKEND_ERRORS=1
        fi
        
        echo ""
        echo "🔒 Escaneando seguridad con Bandit..."
        if bandit -r app/ -q; then
            echo "✅ Bandit: Sin vulnerabilidades de seguridad"
        else
            echo "❌ Bandit: Vulnerabilidades de seguridad encontradas"
            BACKEND_ERRORS=1
        fi
        
        echo ""
        echo "📚 Verificando docstrings con pydocstyle..."
        if pydocstyle app/ --convention=google; then
            echo "✅ pydocstyle: Docstrings bien formateados"
        else
            echo "⚠️ pydocstyle: Algunos docstrings necesitan mejoras (no crítico)"
        fi
        
        echo ""
        echo "🧟 Buscando código muerto con Vulture..."
        if vulture app/ --min-confidence 60; then
            echo "✅ Vulture: Sin código muerto detectado"
        else
            echo "⚠️ Vulture: Posible código muerto encontrado (revisar manualmente)"
        fi
        
        echo ""
        echo "🛡️ Verificando dependencias con Safety..."
        if safety check -r requirements.txt; then
            echo "✅ Safety: Sin vulnerabilidades en dependencias"
        else
            echo "❌ Safety: Vulnerabilidades en dependencias encontradas"
            BACKEND_ERRORS=1
        fi
        
        echo ""
        echo "🧪 Ejecutando tests..."
        if pytest --quiet; then
            echo "✅ Tests: Todos pasaron"
        else
            echo "❌ Tests: Algunos tests fallaron"
            BACKEND_ERRORS=1
        fi
    fi
    
    cd ../..
else
    echo "⚠️  Directorio backend/credit_management no encontrado"
    BACKEND_ERRORS=1
fi

# Frontend - Next.js/TypeScript
echo ""
echo "🌐 Verificando frontend (Next.js/TypeScript)..."
echo "------------------------------------------------"

if [[ -d "frontend" ]]; then
    cd frontend
    
    # Verificar node_modules
    if [[ ! -d "node_modules" ]]; then
        echo "📥 Instalando dependencias de npm..."
        npm install --silent
    fi
    
    echo "🎨 Verificando formato con Prettier..."
    if npm run format:check --silent; then
        echo "✅ Prettier: Código correctamente formateado"
    else
        echo "❌ Prettier: Código necesita formateo"
        FRONTEND_ERRORS=1
    fi
    
    echo ""
    echo "🔍 Ejecutando ESLint (modo estricto)..."
    if npm run lint:strict --silent; then
        echo "✅ ESLint: Sin errores de estilo (0 warnings)"
    else
        echo "❌ ESLint: Errores o warnings encontrados"
        FRONTEND_ERRORS=1
    fi
    
    echo ""
    echo "🏷️ Verificando tipos con TypeScript..."
    if npm run type-check --silent; then
        echo "✅ TypeScript: Sin errores de tipos"
    else
        echo "❌ TypeScript: Errores de tipos encontrados"
        FRONTEND_ERRORS=1
    fi
    
    echo ""
    echo "🏗️ Verificando build..."
    if npm run build --silent; then
        echo "✅ Build: Compilación exitosa"
    else
        echo "❌ Build: Errores de compilación"
        FRONTEND_ERRORS=1
    fi
    
    echo ""
    echo "🔒 Auditoria de seguridad..."
    if npm run audit:security --silent; then
        echo "✅ NPM Audit: Sin vulnerabilidades críticas"
    else
        echo "❌ NPM Audit: Vulnerabilidades encontradas"
        FRONTEND_ERRORS=1
    fi
    
    echo ""
    echo "📦 Verificando dependencias obsoletas..."
    if npm run check-deps --silent; then
        echo "✅ Dependencies: Todas actualizadas"
    else
        echo "⚠️ Dependencies: Algunas dependencias están obsoletas (no crítico)"
    fi
    
    # Verificar si existen tests
    if [[ -f "package.json" ]] && grep -q '"test"' package.json; then
        echo ""
        echo "🧪 Ejecutando tests..."
        if npm test --silent; then
            echo "✅ Tests: Todos pasaron"
        else
            echo "❌ Tests: Algunos tests fallaron"
            FRONTEND_ERRORS=1
        fi
    else
        echo "⚠️  No se encontraron scripts de test configurados"
    fi
    
    cd ..
else
    echo "⚠️  Directorio frontend no encontrado"
    FRONTEND_ERRORS=1
fi

# Resumen final
echo ""
echo "📊 Resumen de Verificación"
echo "=========================="

if [[ $BACKEND_ERRORS -eq 0 ]]; then
    echo "✅ Backend: Todos los checks pasaron"
else
    echo "❌ Backend: Errores encontrados"
fi

if [[ $FRONTEND_ERRORS -eq 0 ]]; then
    echo "✅ Frontend: Todos los checks pasaron"
else
    echo "❌ Frontend: Errores encontrados"
fi

# Determinar estado final
TOTAL_ERRORS=$((BACKEND_ERRORS + FRONTEND_ERRORS))

if [[ $TOTAL_ERRORS -eq 0 ]]; then
    echo ""
    echo "🎉 ¡Verificación completada exitosamente!"
    echo "El código cumple con todos los estándares."
    echo ""
    echo "📋 Listo para:"
    echo "  - Hacer commit"
    echo "  - Crear pull request"
    echo "  - Desplegar a producción"
    echo ""
    exit 0
else
    echo ""
    echo "❌ Verificación falló con $TOTAL_ERRORS error(es)"
    echo "Por favor, revisa y corrige los errores antes de continuar."
    echo ""
    echo "💡 Sugerencias:"
    echo "  1. Ejecutar: ./scripts/format-all.sh"
    echo "  2. Revisar errores específicos arriba"
    echo "  3. Ejecutar tests individuales para más detalles"
    echo ""
    exit 1
fi
