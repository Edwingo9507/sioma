"""
Test rápido para verificar que las pantallas se cargan correctamente
"""
import sys
sys.path.insert(0, '.')

# Mock de cv2 y sklearn si no están disponibles
try:
    import cv2
except ImportError:
    print("OpenCV no disponible - modo de prueba sin cámara")

try:
    from sklearn.neighbors import KNeighborsClassifier
except ImportError:
    print("scikit-learn no disponible - modo de prueba sin clasificador")

from main import SinomaApp, MenuScreen, RegisterFaceScreen, AttendanceScreen
from kivy.uix.screenmanager import ScreenManager

def test_screens():
    """Verifica que las pantallas se puedan crear sin errores"""
    print("Probando creación de pantallas...")
    
    try:
        sm = ScreenManager()
        
        menu_screen = MenuScreen(name='menu')
        print("✓ MenuScreen creado")
        
        register_screen = RegisterFaceScreen(name='register')
        print("✓ RegisterFaceScreen creado")
        
        attendance_screen = AttendanceScreen(name='attendance')
        print("✓ AttendanceScreen creado")
        
        sm.add_widget(menu_screen)
        sm.add_widget(register_screen)
        sm.add_widget(attendance_screen)
        print("✓ Todas las pantallas agregadas al ScreenManager")
        
        # Verificar que se pueden obtener por nombre
        assert sm.get_screen('menu') == menu_screen
        assert sm.get_screen('register') == register_screen
        assert sm.get_screen('attendance') == attendance_screen
        print("✓ Todas las pantallas son accesibles por nombre")
        
        print("\n✅ TODAS LAS PRUEBAS PASARON - La app debería funcionar correctamente")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # No ejecutar la app completa, solo probar la estructura
    print("=" * 60)
    print("TEST DE ESTRUCTURA DE PANTALLAS - SINOMA")
    print("=" * 60)
    test_screens()
