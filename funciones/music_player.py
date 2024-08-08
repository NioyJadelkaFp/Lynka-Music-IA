import threading
import random
import time
from youtube_utils import play_youtube_video, get_video_duration
from browser_utils import open_video_in_browser, close_window

random_songs = ["rara vez", "rain 3", "rain 1", "rain 3"]
is_reproducing = False  # Indicador de reproducción
current_timer = None  # Temporizador actual

def play_random_song():
    """Reproducir una canción al azar y esperar a que termine."""
    global is_reproducing, current_timer
    is_reproducing = True  # Marcar como en reproducción
    random_song = random.choice(random_songs)
    video_url, title = play_youtube_video(random_song)
    if video_url:
        open_video_in_browser(video_url)  # Abre el video en el navegador
        duration = get_video_duration(video_url)
        if duration > 0:
            # Crear un temporizador para cerrar la ventana cuando la canción termine
            if current_timer:
                current_timer.cancel()  # Cancelar cualquier temporizador existente
            current_timer = threading.Timer(duration, close_window)
            current_timer.start()
            time.sleep(duration)  # Esperar hasta que termine la canción
    is_reproducing = False  # Marcar como no en reproducción

def process_command(command):
    """Procesar el comando usando IA."""
    global is_reproducing
    if 'reproduce' in command:
        musica = command.replace('reproduce', '').strip()
        print(f'Música: {musica}')
        talk(f'Reproduciendo {musica}')
        if is_reproducing:
            talk("Canción actual detenida.")
            close_window()  # Cerrar la ventana actual si ya está en reproducción
        video_url, title = play_youtube_video(musica)
        if video_url:
            open_video_in_browser(video_url)  # Abre el video en el navegador
            duration = get_video_duration(video_url)
            if duration > 0:
                time.sleep(duration)  # Esperar hasta que termine la canción
    elif 'dj' in command:
        if is_reproducing:
            talk("Deteniendo la música actual.")
            close_window()  # Cerrar la ventana actual
            is_reproducing = False  # Marcar como no en reproducción
        play_random_song()  # Reproducir una nueva canción al azar
    elif 'pausa' in command:
        if is_reproducing:
            talk("La música está en pausa.")
            # Aquí podrías manejar la pausa si tu reproductor lo permitiera
            # Para pywebview, no se puede pausar directamente
        else:
            talk("No hay música para pausar.")
    elif 'salir' in command:
        exit()
    else:
        talk("No entiendo el comando")
