# SINOMA - Sistema de Asistencia con Reconocimiento Facial

Aplicación Android desarrollada con Kivy para registro de asistencia mediante reconocimiento facial usando la cámara del dispositivo.

## 📱 Características

1. **Registrar Rostro**: Captura 100 muestras del rostro de una persona y las almacena para reconocimiento futuro
2. **Tomar Asistencia**: Usa la cámara para reconocer rostros y guardar la asistencia en archivo .txt
3. **Interfaz Simple**: Menú principal con 3 opciones claras y fáciles de usar

## 🔧 Requisitos Previos

### Para desarrollo en escritorio (testing)
```powershell
pip install kivy numpy scikit-learn opencv-python pillow
```

### Para compilar APK de Android
- Python 3.8+
- Buildozer (Linux/WSL) o Bulldozer (alternativa para Windows)
- Android SDK y NDK (se descargan automáticamente con buildozer)

## 📦 Instalación

### 1. Clonar/Descargar el proyecto
El proyecto debe contener:
```
sioma/
├── main.py                    # Aplicación Kivy principal
├── builder.spec               # Configuración de buildozer
├── requirements.txt           # Dependencias Python
├── data/
│   └── haarcascade_frontalface_default.xml  # Clasificador de rostros
├── Attendance/               # Se creará automáticamente
└── README.md
```

### 2. Instalar dependencias para testing local
```powershell
cd sioma
pip install -r requirements.txt
```

## 🚀 Uso

### Testing en escritorio (Windows)
```powershell
cd sioma
python main.py
```

**Nota**: En Windows, la cámara puede tener problemas de permisos. Asegúrate de que Python tiene acceso a la cámara en Configuración > Privacidad.

### Compilar para Android

#### Opción A: Linux/WSL (Recomendado)
```bash
# Instalar buildozer
pip install buildozer

# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Compilar APK (primera vez tarda ~30-60 min)
cd sioma
buildozer android debug

# El APK estará en: bin/myapp-0.1-arm64-v8a_armeabi-v7a-debug.apk
```

#### Opción B: GitHub Actions / CI (sin necesidad de Linux local)
Puedes usar GitHub Actions para compilar el APK en la nube. Crea `.github/workflows/build.yml`:

```yaml
name: Build Android APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        with:
          workdir: sioma
          buildozer_version: stable
      - name: Upload APK
        uses: actions/upload-artifact@v2
        with:
          name: apk
          path: sioma/bin/*.apk
```

## 📱 Uso en Android

### Primera vez:
1. Instalar el APK en tu dispositivo Android
2. Dar permisos de cámara y almacenamiento cuando se soliciten
3. Abrir la app

### Registrar personas:
1. Menú principal → **"1. Registrar Rostro"**
2. Ingresar el nombre de la persona
3. Presionar **"Iniciar Captura"**
4. Mirar a la cámara mientras captura 100 muestras (tarda ~10-15 segundos)
5. Cuando termine, los datos se guardan automáticamente
6. Volver al menú

### Tomar asistencia:
1. Menú principal → **"2. Tomar Asistencia"**
2. Presionar **"Iniciar Cámara"**
3. La app reconocerá automáticamente los rostros registrados
4. Cuando reconozca a alguien, presionar **"Guardar Asistencia"**
5. La asistencia se guarda en: `Attendance/Attendance_DD-MM-YYYY.txt`

## 📄 Formato del archivo de asistencia

Los archivos se guardan en `Attendance/Attendance_<fecha>.txt` con el formato:
```
Juan Perez - 14:30:25
Maria Garcia - 14:31:10
Juan Perez - 15:45:00
```

Cada línea contiene: `Nombre - Hora`

## 🛠️ Estructura del Código

### main.py
- **MenuScreen**: Pantalla principal con menú de 3 opciones
- **RegisterFaceScreen**: Captura 100 muestras faciales y las guarda
- **AttendanceScreen**: Reconoce rostros y guarda asistencia en .txt
- **SinomaApp**: Clase principal de la aplicación Kivy

### builder.spec (buildozer.spec renombrado)
Configuración para compilar el APK:
- **requirements**: opencv,scikit-learn,numpy,kivy,pillow
- **permissions**: CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
- **features**: android.hardware.camera, android.hardware.camera.autofocus
- **android.api**: 31 (Android 12)
- **android.minapi**: 21 (Android 5.0)

## 🔍 Troubleshooting

### La cámara no funciona en desktop
- Windows: Verificar permisos en Configuración > Privacidad > Cámara
- Linux: Verificar que el usuario está en el grupo `video`: `sudo usermod -a -G video $USER`

### Error al compilar con buildozer
- Asegúrate de estar en Linux o WSL (Windows Subsystem for Linux)
- Verifica que tienes suficiente espacio en disco (~10 GB)
- Si falla, intenta: `buildozer android clean` y vuelve a compilar

### La app no reconoce rostros
- Primero debes registrar al menos una persona con "Registrar Rostro"
- Asegúrate de que los archivos `data/names.pkl` y `data/faces_data.pkl` existen
- Verifica que hay buena iluminación al usar la cámara

### Permisos en Android
- Si la app crashea al abrir la cámara, ve a Configuración > Apps > SINOMA > Permisos
- Habilita: Cámara, Almacenamiento

## 📋 Diferencias con versiones anteriores

### Cambios principales:
1. ✅ **GUI con Kivy** (antes: scripts de consola con OpenCV)
2. ✅ **Guarda en .txt** (antes: .csv)
3. ✅ **Menú simple** con 3 opciones claras
4. ✅ **Compatible con Android** (antes: solo desktop)
5. ❌ **Removido Streamlit** (no compatible con Android)
6. ✅ **Permisos de cámara** configurados correctamente

## 🔐 Permisos Android

La app solicita:
- **CAMERA**: Para capturar rostros y reconocimiento facial
- **WRITE_EXTERNAL_STORAGE**: Para guardar archivos de asistencia
- **READ_EXTERNAL_STORAGE**: Para leer datos de rostros guardados

## 📚 Dependencias

### En Android (builder.spec):
- python3
- kivy
- opencv (recipe especial para Android)
- numpy
- scikit-learn
- pillow

### En Desktop (requirements.txt):
- kivy >= 2.2.0
- opencv-python >= 4.5.0
- numpy >= 1.21.0
- scikit-learn >= 1.0.0
- pillow >= 9.0.0

## 🎯 Próximos pasos sugeridos

1. Agregar base de datos SQLite para historial completo
2. Exportar reportes en PDF
3. Agregar foto de perfil a cada persona registrada
4. Modo oscuro / temas personalizables
5. Sincronización con servidor remoto
6. Reconocimiento de múltiples rostros simultáneos

## 📞 Soporte

Si encuentras problemas:
1. Verifica que todos los archivos necesarios estén presentes
2. Revisa los logs de buildozer: `.buildozer/android/platform/build-*/build.log`
3. Asegúrate de tener la última versión de buildozer: `pip install --upgrade buildozer`

## 📝 Licencia

Proyecto de Hackaton II - Android APP

---
**Desarrollado con ❤️ usando Kivy y OpenCV**
