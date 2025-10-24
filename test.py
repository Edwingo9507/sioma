from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime


def speak(str1):
    print(f"SISTEMA: {str1}")




# 1. Verificar y crear la carpeta de Asistencia si no existe
ATTENDANCE_FOLDER = 'Attendance'
if not os.path.isdir(ATTENDANCE_FOLDER):
    os.makedirs(ATTENDANCE_FOLDER)

# 2. Rutas de archivos de datos 
DATA_FOLDER = 'data'
HAARCASCADE_PATH = os.path.join(DATA_FOLDER, 'haarcascade_frontalface_default.xml')
NAMES_PATH = os.path.join(DATA_FOLDER, 'names.pkl')
FACES_PATH = os.path.join(DATA_FOLDER, 'faces_data.pkl')


# --- CARGA DEL MODELO Y DATOS ---

video = cv2.VideoCapture(0)
# Se  forzar la resolución
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# Verifica la existencia del archivo antes de cargarlo
if not os.path.exists(HAARCASCADE_PATH):
    raise FileNotFoundError(f"Error: No se encontró el clasificador en la ruta: {HAARCASCADE_PATH}")

facedetect = cv2.CascadeClassifier(HAARCASCADE_PATH)

# Carga de NOMBRES
try:
    with open(NAMES_PATH, 'rb') as w:
        LABELS = pickle.load(w)
except FileNotFoundError:
    raise FileNotFoundError(f"Error: No se encontró el archivo de nombres. Ejecuta el script de entrenamiento primero. Ruta: {NAMES_PATH}")

# Carga de DATOS FACIALES
try:
    with open(FACES_PATH, 'rb') as f:
        FACES = pickle.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Error: No se encontró la matriz de datos faciales. Ejecuta el script de entrenamiento primero. Ruta: {FACES_PATH}")


print('Shape of Faces matrix --> ', FACES.shape)

knn = KNeighborsClassifier(n_neighbors=5)
# Asegúrese de que FACES y LABELS tienen la misma cantidad de muestras (filas)
knn.fit(FACES, LABELS)

# --- Carga inicial de la imagen de fondo (solo una vez) ---
ORIGINAL_BACKGROUND_IMAGE = None
if not os.path.exists("background.png"):
     print("Advertencia: No se encontró 'background.png'. Se usará solo el video.")
else:
    ORIGINAL_BACKGROUND_IMAGE = cv2.imread("background.png")


COL_NAMES = ['NAME', 'TIME']

# Nuevas variables persistentes para el último reconocimiento válido (soluciona el error de timing al presionar 'o')
last_recognized_name = "Unknown"
last_recognized_time = "N/A"
last_recognized_date = "N/A"

# Variables para control de estado y feedback visual
attendance_status = None # Usado para mostrar 'ASISTENCIA REGISTRADA'
status_timer = 0
# Variables para controlar la visualización del cuadro de detección
detected_face_info = None # (x, y, w, h) de la última cara detectada
detection_timer = 0 # Contador para el tiempo de visualización del cuadro


# --- BUCLE PRINCIPAL ---

while True:
    # ------------------------------------------------------------------
    # MANEJO DE TIMERS
    # ------------------------------------------------------------------
    
    # 1. Timer para el mensaje de ASISTENCIA REGISTRADA (50, 50)
    if attendance_status is not None:
        status_timer += 1
        if status_timer > 30: 
            attendance_status = None
            status_timer = 0
            
    # 2. Timer para el CUADRO DE DETECCIÓN
    if detected_face_info is not None:
        detection_timer += 1
        # El cuadro se muestra por 20 frames (~0.6 segundos) después de la última detección
        if detection_timer > 20: 
            detected_face_info = None
            
    ret, frame = video.read()
    if not ret:
        print("Error al leer el frame de la cámara. Saliendo.")
        break
    
    # =========================================================================
    
    # AJUSTADO: Redimensionar el frame de la cámara al tamaño exacto que el slot en el fondo permite (640x414)
    frame = cv2.resize(frame, (640, 414))
    # =========================================================================
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    

    # Recargar la imagen de fondo en CADA FRAME para limpiarla de dibujos anteriores
    if ORIGINAL_BACKGROUND_IMAGE is None:
        display_frame = frame
    else:
        # Crea una copia limpia de la imagen de fondo original
        display_frame = ORIGINAL_BACKGROUND_IMAGE.copy() 
        # Ahora las dimensiones de 'frame' (640x414x3) coinciden con el área de destino.
        # Ajustamos el área de pegado para que coincida con la nueva altura: 414
        display_frame[162:162 + 414, 55:55 + 640] = frame
    # --- FIN DE LA SOLUCIÓN ---
    
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        
        ts = time.time()
        
        # --- ACTUALIZACIÓN DE ESTADO PERSISTENTE ---
        # Si se detecta una cara, actualizamos el último estado válido y reiniciamos el timer visual
        last_recognized_name = str(output[0])
        last_recognized_time = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        last_recognized_date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        
        # Guardamos las coordenadas y reiniciamos el timer de visualización
        detected_face_info = (x, y, w, h)
        detection_timer = 0
        
  
    # Informacion visual para 
 
    
    # Dibuja el cuadro si se ha detectado un nombre válido
    if detected_face_info is not None and last_recognized_name != "Unknown":
        x, y, w, h = detected_face_info
        
        # Dibujar rectángulos y texto
        cv2.rectangle(display_frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(display_frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        # Usar el nombre de la variable persistente
        cv2.putText(display_frame, last_recognized_name, (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

    # Dibuja el mensaje de ASISTENCIA REGISTRADA
    if attendance_status is not None:
        # Posición para el mensaje de asistencia (se dibuja en la parte superior izquierda del video)
        cv2.putText(display_frame, attendance_status, (55, 150), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)


    cv2.imshow("Frame", display_frame)
    k = cv2.waitKey(1)
    
    if k == ord('o'):
        # La asistencia solo se registra si se ha reconocido a alguien recientemente
        if last_recognized_name != "Unknown":
            speak("Attendance Taken..")
            
            attendance_status = f"ASISTENCIA REGISTRADA: {last_recognized_name}" 
            status_timer = 0 # Reinicia el contador para mostrar el mensaje
            
            # Archivo CSV de asistencia para la fecha de la última detección válida
            attendance_file_path = os.path.join(ATTENDANCE_FOLDER, "Attendance_" + last_recognized_date + ".csv")
            exist = os.path.isfile(attendance_file_path)
            
            # Datos a escribir: nombre y hora de la última detección
            data_to_write = [last_recognized_name, last_recognized_time]
            
            if exist:
                with open(attendance_file_path, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(data_to_write)
            else:
                with open(attendance_file_path, "w", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerow(data_to_write)
        else:
            print("No se detectó ninguna cara VÁLIDA para registrar asistencia.")

    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
