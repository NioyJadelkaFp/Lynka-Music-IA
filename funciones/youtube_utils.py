import yt_dlp

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
            duration = info.get('duration', 0)
            return duration
        except Exception as e:
            print("Error al obtener la duración del video:", str(e))
            return 0

def play_youtube_video(query):
    """Buscar y obtener la URL de un video de YouTube"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            video_url = info['url']
            title = info['title']
            return video_url, title
        except Exception as e:
            print("Error al obtener la URL del video:", str(e))
            return None, None
