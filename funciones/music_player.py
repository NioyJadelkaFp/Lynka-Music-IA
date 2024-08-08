import threading
import random
import time
from funciones.speech_utils import listen, talk
from funciones.youtube_utils import play_youtube_video, get_video_duration
from funciones.browser_utils import open_video_in_browser, close_window

random_songs = ["rara vez", "rain 3", "rain 1", "rain 3"]
is_reproducing = False
current_timer = None

def play_random_song():
    """Reproducir una canción al azar y esperar a que termine."""
    global is_reproducing, current_timer
    is_reproducing = True
    random_song = random.choice(random_songs)
    video_url, title = play_youtube_video(random_song)
    if video_url:
        open_video_in_browser(video_url)
        duration = get_video_duration(video_url)
        if duration > 0:
            if current_timer:
                current_timer.cancel()
            current_timer = threading.Timer(duration, close_window)
            current_timer.start()
            time.sleep(duration)
    is_reproducing = False

def process_command(command):
    """Procesar el comando usando IA."""
    global is_reproducing
    if 'reproduce' in command:
        musica = command.replace('reproduce', '').strip()
        talk(f'Reproduciendo {musica}')
        if is_reproducing:
            talk("Canción actual detenida.")
            close_window()
        video_url, title = play_youtube_video(musica)
        if video_url:
            open_video_in_browser(video_url)
            duration = get_video_duration(video_url)
            if duration > 0:
                time.sleep(duration)
    elif 'dj' in command:
        if is_reproducing:
            talk("Deteniendo la música actual.")
            close_window()
            is_reproducing = False
        play_random_song()
    elif 'pausa' in command:
        if is_reproducing:
            talk("La música está en pausa.")
        else:
            talk("No hay música para pausar.")
    elif 'salir' in command:
        exit()
    else:
        talk("No entiendo el comando")
