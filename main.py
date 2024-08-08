from funciones.speech_utils import listen, talk
from funciones.music_player import process_command

def run_dj():
    """Ciclo principal del asistente."""
    while True:
        rec = listen()
        if rec:
            process_command(rec)

if __name__ == '__main__':
    run_dj()
