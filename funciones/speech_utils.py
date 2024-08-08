import speech_recognition as sr
import pyttsx3

name = "dj"
listener = sr.Recognizer()
engine = pyttsx3.init()

# Configurar la voz del asistente
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)

def talk(text):
    """Convertir texto a voz."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Escuchar y reconocer comandos de voz."""
    rec = ""
    if not is_reproducing:  # Solo escuchar si no está en reproducción
        try:
            with sr.Microphone() as source:
                print("Escuchando...")
                listener.adjust_for_ambient_noise(source)  # Ajustar para ruidos de fondo
                pc = listener.listen(source)
                rec = listener.recognize_google(pc, language='es-ES')  # Reconocer en español
                rec = rec.lower()
                if name in rec:
                    rec = rec.replace(name, '')
        except sr.UnknownValueError:
            print("¿Intenta hablar?")
        except sr.RequestError:
            print("No se pudo conectar con el servicio de reconocimiento de voz")
            talk("No se pudo conectar con el servicio de reconocimiento de voz")
    
    return rec
