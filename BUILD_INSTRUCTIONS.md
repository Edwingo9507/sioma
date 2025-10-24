# 📱 INSTRUCCIONES DE COMPILACIÓN - SINOMA APK

## ✅ CONFIGURACIÓN COMPLETA - buildozer.spec

El archivo `buildozer.spec` está completamente configurado con:

### 📋 Configuración General
- **Título**: SINOMA APP
- **Package**: org.test.myapp
- **Versión**: 0.1
- **Orientación**: portrait (vertical)

### 📦 Archivos Incluidos
```ini
source.include_exts = py,png,jpg,kv,atlas,xml,pkl
source.include_patterns = data/*,Attendance/*
```
✅ Incluye:
- Todos los archivos Python (.py)
- Logo e imágenes (.png, .jpg)
- Archivos XML (haarcascade_frontalface_default.xml)
- Archivos PKL (datos de rostros y nombres)
- Carpeta data/ completa
- Carpeta Attendance/ para guardar asistencias

### 📦 Dependencias (requirements)
```ini
requirements = python3==3.9.9,kivy==2.2.1,numpy,opencv,scikit-learn,pillow
```

**IMPORTANTE**: 
- ✅ `opencv` (no `opencv-python` - es una receta especial para Android)
- ✅ `python3==3.9.9` y `kivy==2.2.1` (versiones compatibles con buildozer)

### 🔐 Permisos Android
```ini
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
```

- **CAMERA**: Captura de rostros y reconocimiento facial
- **WRITE_EXTERNAL_STORAGE**: Guardar archivos .txt de asistencia
- **READ_EXTERNAL_STORAGE**: Leer archivos .pkl de rostros guardados
- **INTERNET**: Para futuras actualizaciones (opcional)

### 📷 Features de Hardware
```ini
android.features = android.hardware.camera,android.hardware.camera.autofocus
```
- Requiere cámara con autofocus

### 🎯 APIs Android
```ini
android.api = 31          # Target API (Android 12)
android.minapi = 21       # Mínimo API (Android 5.0 Lollipop)
android.ndk = 25b         # NDK version
android.ndk_api = 21
```

### 🏗️ Arquitecturas
```ini
android.archs = arm64-v8a, armeabi-v7a
```
- Compatible con la mayoría de dispositivos Android modernos

### 💾 Almacenamiento
```ini
android.private_storage = True
android.allow_backup = True
```
- Datos privados de la app
- Backup automático habilitado

---

## 🚀 CÓMO COMPILAR EL APK

### Opción 1: Linux / WSL (RECOMENDADO)

#### 1. Instalar dependencias del sistema
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake \
    libffi-dev libssl-dev

# Instalar buildozer
pip3 install --upgrade buildozer cython
```

#### 2. Navegar a la carpeta del proyecto
```bash
cd /path/to/sioma
```

#### 3. Primera compilación (tarda ~30-60 minutos)
```bash
buildozer android debug
```

#### 4. Compilaciones posteriores (más rápidas)
```bash
buildozer android debug
```

#### 5. Encontrar el APK
El APK estará en:
```
bin/myapp-0.1-arm64-v8a_armeabi-v7a-debug.apk
```

---

### Opción 2: GitHub Actions (Sin necesidad de Linux)

Crea `.github/workflows/build-apk.yml`:

```yaml
name: Build Android APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        with:
          workdir: sioma
          buildozer_version: stable
      
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: SINOMA-APK
          path: sioma/bin/*.apk
```

Luego:
1. Haz push a GitHub
2. Ve a Actions → Build Android APK → Run workflow
3. Descarga el APK desde Artifacts cuando termine

---

### Opción 3: Docker (Multiplataforma)

```bash
# Pull imagen con buildozer
docker pull kivy/buildozer

# Compilar
docker run --rm -v "$(pwd)":/home/user/hostcwd kivy/buildozer \
    android debug
```

---

## 📱 INSTALAR EN ANDROID

### Desde PC vía ADB
```bash
# Habilitar depuración USB en el teléfono
# Conectar teléfono al PC

adb install -r bin/myapp-0.1-arm64-v8a_armeabi-v7a-debug.apk
```

### Transferencia directa
1. Transferir el APK al teléfono (cable USB, Bluetooth, email, etc.)
2. En el teléfono: Configuración → Seguridad → Permitir instalación de fuentes desconocidas
3. Abrir el APK desde el administrador de archivos
4. Seguir el asistente de instalación

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "Command failed: python -m pythonforandroid.toolchain"
- **Solución**: Asegúrate de estar en Linux/WSL, no Windows
- Verifica que tienes Java instalado: `java -version`

### Error: "No space left on device"
- **Solución**: Necesitas al menos 10 GB libres
- Limpia compilaciones anteriores: `buildozer android clean`

### Error: "SDK license not accepted"
- **Solución**: Ya está configurado `android.accept_sdk_license = True`
- Si persiste: `buildozer android clean` y vuelve a compilar

### Error al compilar opencv
- **Solución**: Asegúrate de usar `opencv` (no `opencv-python`)
- Puede tardar mucho tiempo (30+ minutos) la primera vez

### APK instalado pero crashea al abrir
- Verifica permisos en: Configuración → Apps → SINOMA → Permisos
- Habilita: Cámara, Almacenamiento
- Revisa logs: `adb logcat | grep python`

### Cámara no funciona en el teléfono
- Asegúrate de dar permisos de cámara cuando la app lo solicite
- Verifica que otros apps pueden usar la cámara
- Algunos teléfonos requieren reiniciar después de dar permisos

---

## 📊 COMANDOS ÚTILES DE BUILDOZER

```bash
# Limpiar compilaciones anteriores
buildozer android clean

# Compilar APK de release (firmado)
buildozer android release

# Ver dispositivos conectados
buildozer android adb -- devices

# Instalar APK directamente
buildozer android deploy run

# Ver logs en tiempo real
buildozer android logcat

# Actualizar buildozer
pip install --upgrade buildozer

# Listar targets disponibles
buildozer --version
```

---

## 🔍 VERIFICAR ANTES DE COMPILAR

✅ Checklist:
- [ ] Archivo `main.py` sin errores de sintaxis
- [ ] Carpeta `data/` con `haarcascade_frontalface_default.xml`
- [ ] Logo `logo.png` en la carpeta raíz del proyecto
- [ ] `buildozer.spec` configurado correctamente
- [ ] Estás en Linux/WSL (no Windows)
- [ ] Tienes al menos 10 GB de espacio libre
- [ ] Java 17 instalado (`java -version`)
- [ ] Python 3.8+ instalado (`python3 --version`)

---

## 📁 ESTRUCTURA FINAL PARA COMPILAR

```
sioma/
├── main.py                    ⭐ App principal
├── buildozer.spec            ⭐ Configuración (este archivo)
├── logo.png                  ⭐ Icono de la app (debe existir)
│
├── data/
│   └── haarcascade_frontalface_default.xml  ⭐ Detector de rostros
│
├── Attendance/               (se crea automáticamente)
│
└── .buildozer/              (se crea al compilar)
    └── android/
        └── platform/
            └── build-*/
                └── dists/
                    └── myapp/
                        └── build/
                            └── outputs/
                                └── apk/
```

---

## 🎉 APK FINAL

Cuando termine la compilación, encontrarás:
- **Ubicación**: `sioma/bin/myapp-0.1-arm64-v8a_armeabi-v7a-debug.apk`
- **Tamaño**: ~50-80 MB (aproximado)
- **Compatible con**: Android 5.0+ (API 21+)
- **Arquitecturas**: ARM 32-bit y 64-bit

---

## 📞 NOTAS FINALES

### Primera compilación
- Descarga Android SDK (~500 MB)
- Descarga Android NDK (~800 MB)
- Compila dependencias (opencv, numpy, etc.)
- **Tiempo total**: 30-60 minutos

### Compilaciones siguientes
- Solo recompila lo que cambió
- **Tiempo**: 5-10 minutos

### Testing
1. ⚠️ **Siempre prueba primero en desktop**: `python main.py`
2. ✅ Si funciona en desktop, compila para Android
3. 📱 Instala y prueba en un dispositivo real

---

**¡El buildozer.spec está listo para compilar! 🚀**
