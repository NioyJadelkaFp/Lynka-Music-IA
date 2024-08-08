import spacy
import threading
import random
import time
import webview
import pyttsx3
import speech_recognition as sr
import yt_dlp


try:
    nlp = spacy.load("es_core_news_sm")
    print("Modelo cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")


# Inicializar el modelo spaCy y otros componentes
engine = pyttsx3.init()
listener = sr.Recognizer()

# Configurar la voz del asistente
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)

# Lista de canciones al azar
random_songs = ["rara vez", "rain 3", "rain 1", "rain 3"]

is_reproducing = False  # Indicador de reproducción
current_window = None  # Ventana actual del navegador
current_timer = None  # Temporizador actual

def talk(text):
    """Convertir texto a voz"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Escuchar y reconocer comandos de voz"""
    rec = ""
    if not is_reproducing:  # Solo escuchar si no está en reproducción
        try:
            with sr.Microphone() as source:
                print("escuchando..")
                listener.adjust_for_ambient_noise(source)  # Ajustar para ruidos de fondo
                pc = listener.listen(source)
                rec = listener.recognize_google(pc, language='es-ES')  # Reconocer en español
                rec = rec.lower()
        except sr.UnknownValueError:
            print("intenda hablar?")
        except sr.RequestError:
            print("No se pudo conectar con el servicio de reconocimiento de voz")
            talk("No se pudo conectar con el servicio de reconocimiento de voz")
    
    return rec

def get_video_duration(url):
    """Obtener la duración del video en segundos"""
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'format': 'bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            duration = info.get('duration', 0)  # Usar .get() para evitar errores si 'duration' no está presente
            return duration
        except Exception as e:
            print("Error al obtener la duración del video:", str(e))
            return 0

def play_youtube_video(query):
    """Reproducir video de YouTube en el navegador con pywebview"""
    global current_window
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            video_url = info['url']  # Obtener la URL del video
            print(f"Reproduciendo: {info['title']}")
            talk(f"Reproduciendo {info['title']}")
            
            # Cerrar la ventana actual (si es que hay una abierta)
            if current_window:
                current_window.eval('window.close()')  # Cierra la ventana actual en pywebview
            
            # Crear una nueva ventana y abrir el video
            current_window = webview.create_window('Reproductor de Música', video_url)
            webview.start()
            
            duration = get_video_duration(video_url)  # Obtener la duración del video
            return duration
        except Exception as e:
            talk("Hubo un problema al reproducir el video")
            print("Error al reproducir el video:", str(e))
            return 0

def play_random_song():
    """Reproducir una canción al azar y esperar a que termine"""
    global is_reproducing, current_timer
    is_reproducing = True  # Marcar como en reproducción
    random_song = random.choice(random_songs)
    duration = play_youtube_video(random_song)
    if duration > 0:
        # Crear un temporizador para cerrar la ventana cuando la canción termine
        if current_timer:
            current_timer.cancel()  # Cancelar cualquier temporizador existente
        current_timer = threading.Timer(duration, close_window)
        current_timer.start()
        time.sleep(duration)  # Esperar hasta que termine la canción
    is_reproducing = False  # Marcar como no en reproducción

def close_window():
    """Cerrar la ventana actual"""
    global current_window
    if current_window:
        current_window.eval('window.close()')  # Cierra la ventana actual en pywebview

def process_command(command):
    """Procesar el comando usando IA"""
    global is_reproducing
    
    doc = nlp(command.lower())
    tokens = [token.text for token in doc]
    
    # Verificar comandos con palabras clave
    if 'reproduce' in tokens:
        musica = ' '.join(tokens[tokens.index('reproduce') + 1:]).strip()
        print(f'Música: {musica}')
        talk(f'Reproduciendo {musica}')
        if is_reproducing:
            talk("Canción actual detenida.")
            close_window()  # Cerrar la ventana actual si ya está en reproducción
        duration = play_youtube_video(musica)
        if duration > 0:
            time.sleep(duration)  # Esperar hasta que termine la canción
    
    elif 'dj' in tokens:
        if is_reproducing:
            talk("Deteniendo la música actual.")
            close_window()  # Cerrar la ventana actual
            is_reproducing = False  # Marcar como no en reproducción
        play_random_song()  # Reproducir una nueva canción al azar
    
    elif 'pausa' in tokens:
        if is_reproducing:
            talk("La música está en pausa.")
        else:
            talk("No hay música para pausar.")
    
    elif 'salir' in tokens:
        exit()
    
    else:
        talk("No entiendo el comando")

def run_dj():
    """Ciclo principal del asistente"""
    while True:
        rec = listen()
        if rec:
            process_command(rec)

if __name__ == '__main__':
    run_dj()
