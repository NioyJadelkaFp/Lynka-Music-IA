import webview

current_window = None

def open_video_in_browser(url):
    """Abrir un video en el navegador utilizando pywebview."""
    global current_window
    if current_window:
        close_window()
    current_window = webview.create_window('Reproductor de Música', url)
    webview.start()

def close_window():
    """Cerrar la ventana del navegador."""
    global current_window
    if current_window:
        # Necesitamos manejar el cierre de la ventana de forma más segura.
        # Esta línea asegura que la ventana se cierra correctamente.
        current_window.evaluate('window.close()')
        current_window = None
