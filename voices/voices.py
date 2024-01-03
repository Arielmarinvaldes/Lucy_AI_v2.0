import pyttsx3


# tipo de voz del asistente
def spanish_voice():
    change_voice(0)
    talk("Esta es mi voz enn Español")


def english_voice():
    change_voice(1)
    talk("this is my voice in english")


def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola soy Lucy")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 145)
engine.setProperty('rate', voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()