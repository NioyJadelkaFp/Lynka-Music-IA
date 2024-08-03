import speech_recognition as sr
import pyttsx3, pywhatkit

name = "dj"

listerner = sr.recognizers()
engine = pyttsx3.init()

voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)