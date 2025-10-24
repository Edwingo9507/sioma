#!/bin/bash
# Script para solucionar el error de libffi en buildozer
# Ejecutar en Linux/WSL antes de compilar con buildozer

echo "============================================"
echo "SOLUCIONANDO ERROR DE LIBFFI EN BUILDOZER"
echo "============================================"

# 1. Instalar dependencias del sistema necesarias
echo ""
echo "[1/5] Instalando herramientas de compilación..."
sudo apt-get update
sudo apt-get install -y \
    libtool \
    libtool-bin \
    automake \
    autoconf \
    pkg-config \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    python3-pip \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential

# 2. Verificar instalación
echo ""
echo "[2/5] Verificando herramientas instaladas..."
which libtool && echo "✅ libtool instalado" || echo "❌ libtool NO instalado"
which autoconf && echo "✅ autoconf instalado" || echo "❌ autoconf NO instalado"
which automake && echo "✅ automake instalado" || echo "❌ automake NO instalado"
which pkg-config && echo "✅ pkg-config instalado" || echo "❌ pkg-config NO instalado"
java -version 2>&1 | head -n 1 && echo "✅ Java instalado" || echo "❌ Java NO instalado"

# 3. Actualizar buildozer
echo ""
echo "[3/5] Actualizando buildozer y Cython..."
pip3 install --upgrade buildozer cython

# 4. Limpiar compilaciones anteriores (opcional pero recomendado)
echo ""
echo "[4/5] ¿Limpiar compilaciones anteriores? (s/n)"
read -r respuesta
if [[ "$respuesta" == "s" || "$respuesta" == "S" ]]; then
    echo "Limpiando..."
    buildozer android clean
    rm -rf .buildozer/android/platform/build-*
    echo "✅ Limpieza completada"
else
    echo "⏭️  Omitiendo limpieza"
fi

# 5. Instrucciones finales
echo ""
echo "[5/5] Instrucciones finales"
echo "============================================"
echo ""
echo "✅ Dependencias instaladas correctamente"
echo ""
echo "Ahora puedes compilar tu APK con:"
echo ""
echo "  cd sioma"
echo "  buildozer android debug"
echo ""
echo "Notas importantes:"
echo "- La primera compilación puede tardar 30-60 minutos"
echo "- Asegúrate de tener al menos 10 GB libres"
echo "- No interrumpas el proceso de compilación"
echo ""
echo "============================================"
