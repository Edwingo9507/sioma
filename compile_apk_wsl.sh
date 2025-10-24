#!/bin/bash
# Script completo para compilar SINOMA APK en WSL
# Ejecutar: bash compile_apk_wsl.sh

# No usar set -e para que no se detenga en errores menores
# set -e

echo "========================================"
echo "  COMPILACIÓN DE SINOMA APK EN WSL"
echo "========================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paso 1: Verificar que estamos en WSL
echo -e "${YELLOW}[1/8] Verificando entorno WSL...${NC}"
if ! grep -qi microsoft /proc/version; then
    echo -e "${RED}❌ Este script debe ejecutarse en WSL (Windows Subsystem for Linux)${NC}"
    exit 1
fi
echo -e "${GREEN}✅ WSL detectado correctamente${NC}"
echo ""

# Paso 2: Actualizar sistema
echo -e "${YELLOW}[2/8] Actualizando sistema...${NC}"
sudo apt-get update -y
echo -e "${GREEN}✅ Sistema actualizado${NC}"
echo ""

# Paso 3: Instalar dependencias principales
echo -e "${YELLOW}[3/8] Instalando dependencias principales...${NC}"
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    zip \
    unzip
echo -e "${GREEN}✅ Dependencias principales instaladas${NC}"
echo ""

# Paso 4: Instalar GStreamer
echo -e "${YELLOW}[4/8] Instalando GStreamer...${NC}"
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good
echo -e "${GREEN}✅ GStreamer instalado${NC}"
echo ""

# Paso 5: Instalar herramientas de compilación críticas (FIX para libffi)
echo -e "${YELLOW}[5/8] Instalando herramientas de compilación (libtool, autoconf, etc.)...${NC}"
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    libsqlite3-dev \
    sqlite3 \
    bzip2 \
    libbz2-dev \
    zlib1g-dev \
    libssl-dev \
    openssl \
    libgdbm-dev \
    libgdbm-compat-dev \
    liblzma-dev \
    libreadline-dev \
    libncursesw5-dev \
    libffi-dev \
    uuid-dev \
    libtool \
    libtool-bin \
    automake \
    autoconf \
    pkg-config \
    openjdk-17-jdk \
    cmake
echo -e "${GREEN}✅ Herramientas de compilación instaladas (libffi fix incluido)${NC}"
echo ""

# Paso 6: Instalar buildozer y Cython
echo -e "${YELLOW}[6/8] Instalando buildozer y Cython...${NC}"
pip3 install --upgrade pip --break-system-packages
pip3 install --upgrade buildozer --break-system-packages
pip3 install cython==0.29.19 --break-system-packages

# Agregar .local/bin al PATH
export PATH="$HOME/.local/bin:$PATH"

# Configurar pip para usar --break-system-packages por defecto
mkdir -p ~/.config/pip
cat > ~/.config/pip/pip.conf << 'EOF'
[global]
break-system-packages = true
EOF

echo -e "${GREEN}✅ Buildozer y Cython instalados${NC}"
echo ""

# Paso 7: Verificar instalación
echo -e "${YELLOW}[7/8] Verificando herramientas instaladas...${NC}"
echo "Python: $(python3 --version)"
echo "Pip: $(pip3 --version)"
echo "Buildozer: $(buildozer --version)"
echo "Java: $(java -version 2>&1 | head -n 1)"
echo "Git: $(git --version)"
which libtool && echo "✅ libtool: $(which libtool)" || echo "❌ libtool no encontrado"
which autoconf && echo "✅ autoconf: $(which autoconf)" || echo "❌ autoconf no encontrado"
which automake && echo "✅ automake: $(which automake)" || echo "❌ automake no encontrado"
echo -e "${GREEN}✅ Verificación completada${NC}"
echo ""

# Paso 8: Navegar al proyecto y compilar
echo -e "${YELLOW}[8/8] Compilando APK...${NC}"
cd "$(dirname "$0")"

# Verificar archivos necesarios
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ Error: main.py no encontrado${NC}"
    exit 1
fi

if [ ! -f "builder.spec" ]; then
    echo -e "${RED}❌ Error: builder.spec no encontrado${NC}"
    exit 1
fi

if [ ! -f "logo.png" ]; then
    echo -e "${RED}❌ Error: logo.png no encontrado${NC}"
    exit 1
fi

if [ ! -f "data/haarcascade_frontalface_default.xml" ]; then
    echo -e "${RED}❌ Error: data/haarcascade_frontalface_default.xml no encontrado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Todos los archivos necesarios encontrados${NC}"
echo ""

# Inicializar buildozer (crear buildozer.spec si no existe)
if [ ! -f "buildozer.spec" ]; then
    echo "Creando buildozer.spec desde builder.spec..."
    cp builder.spec buildozer.spec
fi

echo ""
echo "========================================"
echo "  INICIANDO COMPILACIÓN"
echo "========================================"
echo ""
echo "⏰ NOTA: La primera compilación puede tardar 30-60 minutos"
echo "📦 Se descargarán ~1.5 GB (Android SDK, NDK, dependencias)"
echo "💾 Se necesitan ~10 GB de espacio libre"
echo ""
echo "Presiona ENTER para continuar o Ctrl+C para cancelar..."
read dummy

# Limpiar compilaciones anteriores (opcional)
echo "¿Limpiar compilaciones anteriores? (s/n)"
read -r respuesta
if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
    echo "Limpiando..."
    buildozer android clean 2>/dev/null || echo "No hay compilaciones previas"
    echo -e "${GREEN}✅ Limpieza completada${NC}"
fi

# Compilar APK
echo ""
echo "Iniciando compilación con buildozer..."
echo ""
buildozer -v android debug

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo -e "${GREEN}  ✅ COMPILACIÓN EXITOSA  ${NC}"
    echo "========================================"
    echo ""
    echo "📱 APK generado en:"
    ls -lh bin/*.apk
    echo ""
    echo "Para instalar en Android:"
    echo "  1. Copia el APK a tu teléfono"
    echo "  2. Habilita 'Fuentes desconocidas' en Configuración"
    echo "  3. Abre el APK e instala"
    echo ""
    echo "O usa ADB:"
    echo "  adb install -r bin/*.apk"
    echo ""
else
    echo ""
    echo "========================================"
    echo -e "${RED}  ❌ ERROR EN COMPILACIÓN  ${NC}"
    echo "========================================"
    echo ""
    echo "Revisa los logs arriba para más detalles"
    echo "Errores comunes:"
    echo "  - Falta espacio en disco (necesitas ~10 GB)"
    echo "  - Error de libffi: verifica que libtool esté instalado"
    echo "  - Error de Java: verifica que Java 17 esté instalado"
    echo ""
    exit 1
fi
