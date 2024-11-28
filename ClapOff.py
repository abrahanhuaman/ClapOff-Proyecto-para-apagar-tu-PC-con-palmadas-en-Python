import sounddevice as sd
import numpy as np
import time
import os

# Configuración
FRECUENCIA_MUESTREO = 44100  # Frecuencia de muestreo
DURACION_GRABACION = 0.5     # Duración de la grabación en segundos para cada "escucha"
THRESHOLD = 5                # Umbral reducido para probar con valores más bajos
INTERVALO_PALMADAS = 1.5     # Tiempo máximo en segundos entre palmadas para ser considerado

# Variables para almacenar el tiempo de las palmadas detectadas
ultimo_tiempo = 0
contador_palmadas = 0

def detectar_palmada(indata, frames, tiempo, status):
    """Detecta dos palmadas en un intervalo para apagar la computadora."""
    global ultimo_tiempo, contador_palmadas
    volumen_normalizado = np.mean(np.abs(indata)) * 100  # Promedio absoluto del volumen
    
    if volumen_normalizado > THRESHOLD:  # Si el volumen supera el umbral
        tiempo_actual = time.time()
        
        # Detectar la segunda palmada dentro del intervalo especificado
        if tiempo_actual - ultimo_tiempo < INTERVALO_PALMADAS:
            contador_palmadas += 1
            if contador_palmadas == 2:
                print("¡Detectadas dos palmadas! Apagando el sistema...")
                # Comando para apagar el sistema
                os.system("shutdown /s /t 1")  # Para Windows
                # os.system("shutdown now")  # Para Linux
        else:
            contador_palmadas = 1  # Reiniciar el conteo si el tiempo entre palmadas es demasiado

        ultimo_tiempo = tiempo_actual  # Actualizar el tiempo de la última palmada

def iniciar_escucha():
    """Inicia la escucha continua para detectar las palmadas."""
    with sd.InputStream(callback=detectar_palmada, channels=1, samplerate=FRECUENCIA_MUESTREO):
        print("Escuchando... Da dos palmadas para apagar la computadora.")
        while True:
            time.sleep(DURACION_GRABACION)

# Inicia la detección de palmadas
iniciar_escucha()
