import os
import shutil
import subprocess
import time
import pyautogui  # 🧠 Nuevo import

# --- Configuración ---
ADDON_NAME = "noteDiary"
SOURCE_ADDON_DIR = r"D:\Johan\Documents\GitHub\note-diary\addon"
TARGET_ADDON_DIR = rf"C:\Users\Johan\AppData\Roaming\nvda\addons\{ADDON_NAME}"

print("\n--- Iniciando el proceso de instalación del complemento Note Diary ---\n")

# --- Paso 1: Compilar el complemento con scons ---
print("Compilando el complemento con scons...\n")
try:
    result = subprocess.run("scons", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("\n❌ ¡Error durante la compilación con scons!\n")
        print(result.stdout)
        print(result.stderr)
        input("Presiona Enter para salir . . .")
        exit(result.returncode)
    print("✅ Compilación completada correctamente.\n")
except Exception as e:
    print("\n❌ ¡Error al ejecutar scons!\n")
    print(f"Detalles del error: {str(e)}\n")
    input("Presiona Enter para salir . . .")
    exit(1)

# --- Función para manejo seguro de eliminación de archivos ---
def on_rm_error(func, path, exc_info):
    try:
        os.chmod(path, 0o777)
        func(path)
    except Exception as e:
        print(f"⚠️ No se pudo eliminar: {path}. Se omitirá. Detalles: {e}")

# --- Paso 2: Preparar el directorio de destino ---
print("Preparando el directorio de destino...\n")
try:
    if os.path.exists(TARGET_ADDON_DIR):
        print("Eliminando contenido existente...")
        shutil.rmtree(TARGET_ADDON_DIR, onerror=on_rm_error)
    os.makedirs(TARGET_ADDON_DIR, exist_ok=True)
    print("✅ Directorio de destino creado exitosamente.\n")
except Exception as e:
    print("\n❌ ¡Error al preparar el directorio de destino!\n")
    print(f"Detalles del error: {str(e)}\n")
    input("Presiona Enter para salir . . .")
    exit(1)

# --- Copiar archivos ---
print(f"Copiando archivos desde: {SOURCE_ADDON_DIR} a {TARGET_ADDON_DIR}\n")
try:
    for item in os.listdir(SOURCE_ADDON_DIR):
        s = os.path.join(SOURCE_ADDON_DIR, item)
        d = os.path.join(TARGET_ADDON_DIR, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print("✅ Archivos copiados exitosamente.\n")
except Exception as e:
    print("\n❌ ¡Error al copiar los archivos del complemento!\n")
    print(f"Detalles del error: {str(e)}\n")
    input("Presiona Enter para salir . . .")
    exit(1)

# --- Paso 3: Enviar Insert + Ctrl + F3 con pyautogui ---
print("Esperando 2 segundos antes de enviar la combinación de teclas Insert + Ctrl + F3...\n")
time.sleep(2)

try:
    pyautogui.keyDown('capslock')
    pyautogui.keyDown('ctrl')
    pyautogui.press('f3')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('insert')
    print("✅ Atajo Insert + Ctrl + F3 enviado correctamente.\n")
except Exception as e:
    print("\n⚠️ ¡Error al intentar enviar las teclas con pyautogui!\n")
    print(f"Detalles: {str(e)}\n")

print("--- ✅ Proceso completado correctamente ---\n")
