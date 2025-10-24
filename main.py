"""
SINOMA - Sistema de Asistencia con Reconocimiento Facial
Aplicación Kivy para Android
"""
import os
import pickle
import numpy as np
from datetime import datetime
import time

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger

try:
    import cv2
    from sklearn.neighbors import KNeighborsClassifier
    CV2_AVAILABLE = True
except ImportError as e:
    Logger.warning(f"CV2/SKLearn import error: {e}")
    CV2_AVAILABLE = False


class MenuScreen(Screen):
    """Pantalla principal con el menú de opciones"""
    
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Título
        title = Label(
            text='[b]SINOMA[/b]\nSistema de Asistencia Facial',
            font_size='24sp',
            size_hint=(1, 0.3),
            markup=True
        )
        layout.add_widget(title)
        
        # Botones del menú
        btn_register = Button(
            text='1. Registrar Rostro',
            size_hint=(1, 0.2),
            font_size='18sp'
        )
        btn_register.bind(on_press=self.go_to_register)
        layout.add_widget(btn_register)
        
        btn_attendance = Button(
            text='2. Tomar Asistencia',
            size_hint=(1, 0.2),
            font_size='18sp'
        )
        btn_attendance.bind(on_press=self.go_to_attendance)
        layout.add_widget(btn_attendance)
        
        btn_exit = Button(
            text='3. Salir',
            size_hint=(1, 0.2),
            font_size='18sp',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        btn_exit.bind(on_press=self.exit_app)
        layout.add_widget(btn_exit)
        
        self.add_widget(layout)
    
    def go_to_register(self, instance):
        self.manager.current = 'register'
    
    def go_to_attendance(self, instance):
        self.manager.current = 'attendance'
    
    def exit_app(self, instance):
        App.get_running_app().stop()


class RegisterFaceScreen(Screen):
    """Pantalla para registrar un nuevo rostro"""
    
    def __init__(self, **kwargs):
        super(RegisterFaceScreen, self).__init__(**kwargs)
        
        self.camera = None
        self.faces_data = []
        self.capture_count = 0
        self.is_capturing = False
        self.person_name = ""  # Cambio: era self.name (conflicto con Screen.name)
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        self.title_label = Label(
            text='Registrar Nuevo Rostro',
            size_hint=(1, 0.1),
            font_size='20sp'
        )
        layout.add_widget(self.title_label)
        
        # Input para el nombre
        name_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        name_layout.add_widget(Label(text='Nombre:', size_hint=(0.3, 1)))
        self.name_input = TextInput(
            hint_text='Ingrese su nombre',
            multiline=False,
            size_hint=(0.7, 1)
        )
        name_layout.add_widget(self.name_input)
        layout.add_widget(name_layout)
        
        # Vista de cámara
        self.camera_view = Image(size_hint=(1, 0.5))
        layout.add_widget(self.camera_view)
        
        # Label de estado
        self.status_label = Label(
            text='Ingrese su nombre y presione Iniciar',
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.status_label)
        
        # Botones
        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        self.btn_start = Button(text='Iniciar Captura')
        self.btn_start.bind(on_press=self.start_capture)
        btn_layout.add_widget(self.btn_start)
        
        btn_back = Button(text='Volver al Menú')
        btn_back.bind(on_press=self.go_back)
        btn_layout.add_widget(btn_back)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
    
    def on_enter(self):
        """Se ejecuta al entrar a la pantalla"""
        self.faces_data = []
        self.capture_count = 0
        self.is_capturing = False
        self.name_input.text = ""
        self.status_label.text = 'Ingrese su nombre y presione Iniciar'
    
    def start_capture(self, instance):
        """Inicia la captura de rostros"""
        if not CV2_AVAILABLE:
            self.status_label.text = 'Error: OpenCV no disponible'
            return
        
        self.person_name = self.name_input.text.strip()
        if not self.person_name:
            self.status_label.text = 'Por favor ingrese un nombre'
            return
        
        self.is_capturing = True
        self.faces_data = []
        self.capture_count = 0
        self.btn_start.disabled = True
        self.name_input.disabled = True
        
        # Iniciar cámara
        try:
            self.camera = cv2.VideoCapture(0)
            # Configurar resolución
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # Cargar detector de rostros
            haarcascade_path = 'data/haarcascade_frontalface_default.xml'
            if not os.path.exists(haarcascade_path):
                self.status_label.text = f'Error: No se encontró {haarcascade_path}'
                self.stop_capture()
                return
            
            self.facedetect = cv2.CascadeClassifier(haarcascade_path)
            
            # Iniciar actualización de frames
            Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
            self.status_label.text = f'Capturando... 0/100'
            
        except Exception as e:
            self.status_label.text = f'Error al iniciar cámara: {str(e)}'
            self.stop_capture()
    
    def update_frame(self, dt):
        """Actualiza el frame de la cámara"""
        if not self.is_capturing or self.camera is None:
            return False
        
        ret, frame = self.camera.read()
        if not ret:
            self.status_label.text = 'Error al leer frame'
            self.stop_capture()
            return False
        
        # Detectar rostros
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.facedetect.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w, :]
            resized_img = cv2.resize(crop_img, (50, 50))
            
            # Guardar cada 10 frames
            if len(self.faces_data) < 100 and self.capture_count % 10 == 0:
                self.faces_data.append(resized_img)
                self.status_label.text = f'Capturando... {len(self.faces_data)}/100'
            
            self.capture_count += 1
            
            # Dibujar rectángulo
            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
            cv2.putText(frame, str(len(self.faces_data)), (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 255), 2)
        
        # Verificar si completamos 100 capturas
        if len(self.faces_data) >= 100:
            self.save_faces()
            self.stop_capture()
            return False
        
        # Actualizar imagen en pantalla
        self.display_frame(frame)
        return True
    
    def display_frame(self, frame):
        """Muestra el frame en la interfaz"""
        # Convertir a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Voltear verticalmente
        frame_rgb = cv2.flip(frame_rgb, 0)
        
        # Crear textura
        buf = frame_rgb.tobytes()
        texture = Texture.create(size=(frame_rgb.shape[1], frame_rgb.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.camera_view.texture = texture
    
    def save_faces(self):
        """Guarda los datos de rostros capturados"""
        try:
            os.makedirs('data', exist_ok=True)
            
            faces_array = np.asarray(self.faces_data)
            faces_array = faces_array.reshape(100, -1)
            
            names_path = 'data/names.pkl'
            faces_path = 'data/faces_data.pkl'
            
            # Guardar nombres
            if os.path.exists(names_path):
                with open(names_path, 'rb') as f:
                    names = pickle.load(f)
                names = names + [self.person_name] * 100
            else:
                names = [self.person_name] * 100
            
            with open(names_path, 'wb') as f:
                pickle.dump(names, f)
            
            # Guardar rostros
            if os.path.exists(faces_path):
                with open(faces_path, 'rb') as f:
                    faces = pickle.load(f)
                faces = np.append(faces, faces_array, axis=0)
            else:
                faces = faces_array
            
            with open(faces_path, 'wb') as f:
                pickle.dump(faces, f)
            
            self.status_label.text = f'¡Registro exitoso! {self.person_name} guardado'
            Logger.info(f"RegisterFace: Guardado {self.person_name} con {len(faces_array)} muestras")
            
        except Exception as e:
            self.status_label.text = f'Error al guardar: {str(e)}'
            Logger.error(f"RegisterFace: Error al guardar - {e}")
    
    def stop_capture(self):
        """Detiene la captura"""
        self.is_capturing = False
        if self.camera:
            self.camera.release()
            self.camera = None
        self.btn_start.disabled = False
        self.name_input.disabled = False
        Clock.unschedule(self.update_frame)
    
    def go_back(self, instance):
        """Vuelve al menú principal"""
        self.stop_capture()
        self.manager.current = 'menu'
    
    def on_leave(self):
        """Se ejecuta al salir de la pantalla"""
        self.stop_capture()


class AttendanceScreen(Screen):
    """Pantalla para tomar asistencia con reconocimiento facial"""
    
    def __init__(self, **kwargs):
        super(AttendanceScreen, self).__init__(**kwargs)
        
        self.camera = None
        self.is_running = False
        self.knn = None
        self.last_recognized_name = "Desconocido"
        self.last_recognized_time = ""
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(
            text='Tomar Asistencia',
            size_hint=(1, 0.08),
            font_size='20sp'
        )
        layout.add_widget(title)
        
        # Vista de cámara
        self.camera_view = Image(size_hint=(1, 0.5))
        layout.add_widget(self.camera_view)
        
        # Info de reconocimiento
        self.info_label = Label(
            text='Persona: Desconocido\nÚltimo registro: --',
            size_hint=(1, 0.12),
            font_size='16sp'
        )
        layout.add_widget(self.info_label)
        
        # Label de estado
        self.status_label = Label(
            text='Presione Iniciar para comenzar',
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.status_label)
        
        # Botones
        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        self.btn_start = Button(text='Iniciar Cámara')
        self.btn_start.bind(on_press=self.start_camera)
        btn_layout.add_widget(self.btn_start)
        
        self.btn_save = Button(text='Guardar Asistencia', disabled=True)
        self.btn_save.bind(on_press=self.save_attendance)
        btn_layout.add_widget(self.btn_save)
        
        btn_back = Button(text='Volver')
        btn_back.bind(on_press=self.go_back)
        btn_layout.add_widget(btn_back)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
    
    def on_enter(self):
        """Se ejecuta al entrar a la pantalla"""
        self.last_recognized_name = "Desconocido"
        self.last_recognized_time = ""
        self.update_info_label()
    
    def start_camera(self, instance):
        """Inicia la cámara y el reconocimiento"""
        if not CV2_AVAILABLE:
            self.status_label.text = 'Error: OpenCV no disponible'
            return
        
        # Cargar modelo
        if not self.load_model():
            return
        
        self.is_running = True
        self.btn_start.disabled = True
        self.btn_save.disabled = False
        
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            haarcascade_path = 'data/haarcascade_frontalface_default.xml'
            if not os.path.exists(haarcascade_path):
                self.status_label.text = f'Error: No se encontró {haarcascade_path}'
                self.stop_camera()
                return
            
            self.facedetect = cv2.CascadeClassifier(haarcascade_path)
            Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
            self.status_label.text = 'Cámara activa - Buscando rostros...'
            
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
            self.stop_camera()
    
    def load_model(self):
        """Carga el modelo KNN con los datos guardados"""
        try:
            names_path = 'data/names.pkl'
            faces_path = 'data/faces_data.pkl'
            
            if not os.path.exists(names_path) or not os.path.exists(faces_path):
                self.status_label.text = 'Error: No hay rostros registrados. Registre primero.'
                return False
            
            with open(names_path, 'rb') as f:
                self.labels = pickle.load(f)
            
            with open(faces_path, 'rb') as f:
                self.faces = pickle.load(f)
            
            Logger.info(f"Attendance: Cargados {len(self.labels)} registros")
            
            # Entrenar modelo
            self.knn = KNeighborsClassifier(n_neighbors=5)
            self.knn.fit(self.faces, self.labels)
            
            return True
            
        except Exception as e:
            self.status_label.text = f'Error al cargar modelo: {str(e)}'
            Logger.error(f"Attendance: Error cargando modelo - {e}")
            return False
    
    def update_frame(self, dt):
        """Actualiza el frame y realiza reconocimiento"""
        if not self.is_running or self.camera is None:
            return False
        
        ret, frame = self.camera.read()
        if not ret:
            return True
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.facedetect.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w, :]
            resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
            
            # Predecir
            output = self.knn.predict(resized_img)
            self.last_recognized_name = str(output[0])
            self.last_recognized_time = datetime.now().strftime("%H:%M:%S")
            
            # Dibujar
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, self.last_recognized_name, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            self.update_info_label()
        
        self.display_frame(frame)
        return True
    
    def display_frame(self, frame):
        """Muestra el frame en la interfaz"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.flip(frame_rgb, 0)
        
        buf = frame_rgb.tobytes()
        texture = Texture.create(size=(frame_rgb.shape[1], frame_rgb.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.camera_view.texture = texture
    
    def update_info_label(self):
        """Actualiza el label de información"""
        self.info_label.text = f'Persona: {self.last_recognized_name}\nÚltimo registro: {self.last_recognized_time}'
    
    def save_attendance(self, instance):
        """Guarda la asistencia en archivo TXT"""
        if self.last_recognized_name == "Desconocido" or not self.last_recognized_time:
            self.status_label.text = 'No hay persona reconocida para guardar'
            return
        
        try:
            os.makedirs('Attendance', exist_ok=True)
            
            date = datetime.now().strftime("%d-%m-%Y")
            time_str = datetime.now().strftime("%H:%M:%S")
            txt_path = f'Attendance/Attendance_{date}.txt'
            
            # Guardar en formato de texto simple
            with open(txt_path, 'a', encoding='utf-8') as f:
                f.write(f"{self.last_recognized_name} - {time_str}\n")
            
            self.status_label.text = f'¡Asistencia guardada! {self.last_recognized_name} - {time_str}'
            Logger.info(f"Attendance: Guardado {self.last_recognized_name} a las {time_str}")
            
        except Exception as e:
            self.status_label.text = f'Error al guardar: {str(e)}'
            Logger.error(f"Attendance: Error guardando - {e}")
    
    def stop_camera(self):
        """Detiene la cámara"""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
        self.btn_start.disabled = False
        self.btn_save.disabled = True
        Clock.unschedule(self.update_frame)
    
    def go_back(self, instance):
        """Vuelve al menú principal"""
        self.stop_camera()
        self.manager.current = 'menu'
    
    def on_leave(self):
        """Se ejecuta al salir de la pantalla"""
        self.stop_camera()


class SinomaApp(App):
    """Aplicación principal"""
    
    def build(self):
        # Crear gestor de pantallas
        sm = ScreenManager()
        
        # Agregar las pantallas con verificación
        try:
            menu_screen = MenuScreen(name='menu')
            Logger.info("SinomaApp: MenuScreen creado")
            sm.add_widget(menu_screen)
            Logger.info("SinomaApp: MenuScreen agregado")
            
            register_screen = RegisterFaceScreen(name='register')
            Logger.info("SinomaApp: RegisterFaceScreen creado")
            sm.add_widget(register_screen)
            Logger.info("SinomaApp: RegisterFaceScreen agregado")
            
            attendance_screen = AttendanceScreen(name='attendance')
            Logger.info("SinomaApp: AttendanceScreen creado")
            sm.add_widget(attendance_screen)
            Logger.info("SinomaApp: AttendanceScreen agregado")
            
            # Verificar que las pantallas están registradas
            Logger.info(f"SinomaApp: Pantallas disponibles: {sm.screen_names}")
            
        except Exception as e:
            Logger.error(f"SinomaApp: Error al crear pantallas - {e}")
            import traceback
            traceback.print_exc()
        
        return sm
    
    def on_stop(self):
        """Se ejecuta al cerrar la aplicación"""
        # Limpiar recursos de cámara si están activos
        for screen in self.root.screens:
            if hasattr(screen, 'stop_capture'):
                try:
                    screen.stop_capture()
                except:
                    pass
            if hasattr(screen, 'stop_camera'):
                try:
                    screen.stop_camera()
                except:
                    pass
        return True


if __name__ == '__main__':
    SinomaApp().run()
