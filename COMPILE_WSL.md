# 🚀 COMPILAR SINOMA APK EN WSL (WINDOWS)

## ✅ Opción 1: Script Automático (RECOMENDADO)

### Desde PowerShell (Windows):

```powershell
# Navegar a la carpeta del proyecto
cd "C:\Users\Asus\Documents\Proyectos\Hackaton II\Android APP\sioma"

# Ejecutar script de compilación
.\compile_apk.ps1
```

El script automáticamente:
1. Verifica que WSL esté instalado
2. Verifica los archivos del proyecto
3. Ejecuta la compilación en WSL
4. Te muestra el APK generado

---

## ⚙️ Opción 2: Comandos Manuales en WSL

### 1. Abrir WSL
```powershell
wsl
```

### 2. Navegar al proyecto (ejemplo)
```bash
cd /mnt/c/Users/Asus/Documents/Proyectos/Hackaton\ II/Android\ APP/sioma
```

### 3. Ejecutar script de compilación
```bash
chmod +x compile_apk_wsl.sh
./compile_apk_wsl.sh
```

---

## 📋 Opción 3: Comandos Paso a Paso

Si prefieres ejecutar cada comando manualmente en WSL:

### 1. Actualizar sistema
```bash
sudo apt-get update
```

### 2. Instalar dependencias principales
```bash
sudo apt-get install -y \
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
```

### 3. Instalar GStreamer
```bash
sudo apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good
```

### 4. Instalar herramientas de compilación (FIX libffi)
```bash
sudo apt-get install -y \
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
```

### 5. Instalar buildozer y Cython
```bash
pip3 install --upgrade pip
pip3 install --upgrade buildozer
pip3 install cython==0.29.19
```

### 6. Copiar builder.spec a buildozer.spec
```bash
cp builder.spec buildozer.spec
```

### 7. Limpiar compilaciones anteriores (opcional)
```bash
buildozer android clean
```

### 8. Compilar APK
```bash
buildozer -v android debug
```

---

## 📱 Después de Compilar

El APK estará en: `bin/myapp-0.1-arm64-v8a_armeabi-v7a-debug.apk`

### Instalar en Android:

#### Opción A: Transferencia directa
1. Copia el APK a tu teléfono (USB, email, etc.)
2. En el teléfono: **Configuración → Seguridad → Permitir fuentes desconocidas**
3. Abre el APK desde el administrador de archivos
4. Instala

#### Opción B: Usando ADB
```bash
# En WSL o PowerShell
adb install -r bin/myapp-0.1-arm64-v8a_armeabi-v7a-debug.apk
```

---

## ⏱️ Tiempos de Compilación

- **Primera compilación**: 30-60 minutos
  - Descarga Android SDK (~500 MB)
  - Descarga Android NDK (~800 MB)
  - Compila opencv, numpy, scikit-learn, etc.

- **Compilaciones siguientes**: 5-10 minutos
  - Solo recompila lo que cambió

---

## 💾 Requisitos de Espacio

- **Espacio necesario**: ~10 GB
  - Android SDK: ~2 GB
  - Android NDK: ~2 GB
  - Dependencias compiladas: ~3 GB
  - APK final: ~50-80 MB

---

## 🐛 Solución de Problemas

### Error: "WSL no está instalado"
```powershell
# En PowerShell como Administrador
wsl --install
# Reinicia tu PC y configura Ubuntu
```

### Error: "configure.ac:41: error: possibly undefined macro: AC_PROG_LIBTOOL"
```bash
# Instalar libtool
sudo apt-get install -y libtool libtool-bin automake autoconf
```

### Error: "No space left on device"
```bash
# Limpiar compilaciones anteriores
buildozer android clean
rm -rf .buildozer
```

### Error: "Java not found"
```bash
# Instalar Java 17
sudo apt-get install -y openjdk-17-jdk
java -version  # Verificar
```

### Error: "Permission denied" al ejecutar scripts
```bash
# Dar permisos de ejecución
chmod +x compile_apk_wsl.sh
```

### WSL muy lento o sin espacio
```powershell
# En PowerShell, limpiar WSL
wsl --shutdown
# Luego abre WSL y ejecuta:
sudo apt-get clean
sudo apt-get autoremove
```

---

## 📊 Estructura de Archivos Necesarios

```
sioma/
├── main.py                    ⭐ App Kivy principal
├── builder.spec              ⭐ Configuración buildozer
├── logo.png                  ⭐ Icono (512x512 px recomendado)
├── compile_apk.ps1           ⭐ Script PowerShell
├── compile_apk_wsl.sh        ⭐ Script Bash para WSL
├── data/
│   └── haarcascade_frontalface_default.xml  ⭐ Detector rostros
└── Attendance/               (se crea automáticamente)
```

---

## 🔍 Verificar Instalación

```bash
# En WSL
python3 --version        # Python 3.8+
pip3 --version          # pip actualizado
buildozer --version     # Buildozer instalado
java -version           # Java 17
which libtool           # /usr/bin/libtool
which autoconf          # /usr/bin/autoconf
```

---

## ✅ Checklist Pre-Compilación

- [ ] WSL instalado y configurado
- [ ] Ubuntu en WSL funcionando
- [ ] Al menos 10 GB de espacio libre
- [ ] Archivo `main.py` sin errores
- [ ] Archivo `builder.spec` configurado
- [ ] Logo `logo.png` presente
- [ ] Archivo `data/haarcascade_frontalface_default.xml` presente
- [ ] Internet disponible (para descargas)

---

## 🎉 Próximos Pasos

Una vez compilado exitosamente:

1. **Probar el APK** en un dispositivo real
2. **Dar permisos** de cámara y almacenamiento
3. **Registrar rostros** con la opción 1
4. **Tomar asistencia** con la opción 2
5. **Verificar archivos .txt** en `Attendance/`

---

## 📞 Comandos Útiles

```bash
# Ver logs de compilación
buildozer -v android debug

# Limpiar todo
buildozer android clean
rm -rf .buildozer

# Reinstalar buildozer
pip3 install --upgrade --force-reinstall buildozer

# Ver dispositivos Android conectados
adb devices

# Ver logs de la app en Android
adb logcat | grep python
```

---

**¡Listo para compilar! 🚀**
