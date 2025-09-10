#!/bin/bash

# Script para formatear todo el código del proyecto PrevMora
# Ejecuta las herramientas de formateo en backend y frontend

set -e  # Salir si algún comando falla

echo "🔧 Formateando proyecto completo PrevMora..."
echo "================================================"

# Verificar que estamos en el directorio correcto
if [[ ! -f "README.md" ]] || [[ ! -d "backend" ]] || [[ ! -d "frontend" ]]; then
    echo "❌ Error: Ejecuta este script desde la raíz del proyecto PrevMora"
    exit 1
fi

# Backend - Python/FastAPI
echo ""
echo "📦 Formateando backend (Python/FastAPI)..."
echo "--------------------------------------------"

if [[ -d "backend/credit_management" ]]; then
    cd backend/credit_management
    
    # Verificar que existe el entorno virtual
    if [[ ! -d "venv" ]]; then
        echo "⚠️  No se encontró entorno virtual. Creando..."
        python -m venv venv
    fi
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Instalar herramientas si no están instaladas
    echo "📥 Verificando herramientas de formateo..."
    pip install black isort pylint mypy --quiet
    
    # Formatear código
    echo "🎨 Aplicando Black..."
    black app/ scripts/ --quiet
    
    echo "📑 Organizando imports con isort..."
    isort app/ scripts/ --quiet
    
    echo "✅ Backend formateado correctamente"
    
    cd ../..
else
    echo "⚠️  Directorio backend/credit_management no encontrado"
fi

# Frontend - Next.js/TypeScript
echo ""
echo "🌐 Formateando frontend (Next.js/TypeScript)..."
echo "------------------------------------------------"

if [[ -d "frontend" ]]; then
    cd frontend
    
    # Verificar que existen node_modules
    if [[ ! -d "node_modules" ]]; then
        echo "📥 Instalando dependencias de npm..."
        npm install --silent
    fi
    
    # Formatear código
    echo "🎨 Aplicando Prettier..."
    npm run format --silent
    
    echo "✅ Frontend formateado correctamente"
    
    cd ..
else
    echo "⚠️  Directorio frontend no encontrado"
fi

echo ""
echo "🎉 ¡Formateo completado exitosamente!"
echo "====================================="
echo ""
echo "📋 Próximos pasos recomendados:"
echo "  1. Revisar los cambios: git diff"
echo "  2. Ejecutar verificaciones: ./scripts/check-all.sh"
echo "  3. Ejecutar tests antes del commit"
echo ""
