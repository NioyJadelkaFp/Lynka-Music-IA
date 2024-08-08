import yt_dlp

def get_video_duration(url):
    """Obtener la duración del video en segundos."""
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
    """Reproducir video de YouTube."""
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
            return video_url, info['title']
        except Exception as e:
            talk("Hubo un problema al reproducir el video")
            print("Error al reproducir el video:", str(e))
            return None, None
