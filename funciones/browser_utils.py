import webview

current_window = None  # Ventana actual del navegador

def open_video_in_browser(video_url):
    """Abrir un video en el navegador con pywebview."""
    global current_window
    if current_window:
        current_window.eval('window.close()')  # Cierra la ventana actual en pywebview
    
    current_window = webview.create_window('Reproductor de Música', video_url)
    webview.start()

def close_window():
    """Cerrar la ventana actual."""
    global current_window
    if current_window:
        current_window.eval('window.close()')  # Cierra la ventana actual en pywebview
