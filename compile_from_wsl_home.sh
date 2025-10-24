#!/bin/bash
# Script para compilar desde el home de WSL (sin espacios en la ruta)

echo "========================================"
echo "  COMPILACIÓN DE SINOMA APK"
echo "  (Desde WSL home - sin espacios)"
echo "========================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Crear directorio en home de WSL
PROJECT_DIR="$HOME/sioma_build"
echo -e "${YELLOW}Preparando directorio de compilación...${NC}"
rm -rf "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR"

# Copiar archivos necesarios
echo -e "${YELLOW}Copiando archivos del proyecto...${NC}"
WINDOWS_PROJECT="/mnt/c/Users/Asus/Documents/Proyectos/Hackaton II/Android APP/sioma"

cp "$WINDOWS_PROJECT/main.py" "$PROJECT_DIR/"
cp "$WINDOWS_PROJECT/builder.spec" "$PROJECT_DIR/buildozer.spec"
cp "$WINDOWS_PROJECT/logo.png" "$PROJECT_DIR/"
cp -r "$WINDOWS_PROJECT/data" "$PROJECT_DIR/"

echo -e "${GREEN}✅ Archivos copiados a: $PROJECT_DIR${NC}"
echo ""

# Ir al directorio del proyecto
cd "$PROJECT_DIR"

# Agregar PATH
export PATH="$HOME/.local/bin:$PATH"

# Verificar archivos
echo -e "${YELLOW}Verificando archivos...${NC}"
ls -la
echo ""

echo "========================================"
echo "  INICIANDO COMPILACIÓN"
echo "========================================"
echo ""
echo "⏰ La primera compilación tarda 30-60 minutos"
echo "📦 Se descargarán ~1.5 GB"
echo ""
echo "Presiona ENTER para continuar..."
read

# Compilar
echo -e "${YELLOW}Compilando APK con buildozer...${NC}"
echo ""
buildozer -v android debug

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo -e "${GREEN}  ✅ COMPILACIÓN EXITOSA  ${NC}"
    echo "========================================"
    echo ""
    
    # Copiar APK de vuelta a Windows
    if [ -f "bin/*.apk" ]; then
        echo "Copiando APK a Windows..."
        cp bin/*.apk "$WINDOWS_PROJECT/bin/" 2>/dev/null || mkdir -p "$WINDOWS_PROJECT/bin" && cp bin/*.apk "$WINDOWS_PROJECT/bin/"
        echo -e "${GREEN}✅ APK copiado a: $WINDOWS_PROJECT/bin/${NC}"
        echo ""
        ls -lh "$WINDOWS_PROJECT/bin/"*.apk
    fi
    
    echo ""
    echo "APK generado en WSL:"
    ls -lh bin/*.apk
    echo ""
else
    echo ""
    echo "========================================"
    echo -e "${RED}  ❌ ERROR EN COMPILACIÓN  ${NC}"
    echo "========================================"
    echo ""
    echo "Revisa los logs arriba"
    exit 1
fi
