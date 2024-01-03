import wikipedia
import pywhatkit
import subprocess as sub
import os
import requests
from voices.voices import talk
from diccionary.read import change_data, sites, apps, files

def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 1)
    talk(wiki)


def reproduce(rec):
    music = rec.replace('reproduce', '')
    talk(f"Reproduciendo {music}")
    pywhatkit.playonyt(music)


def abre(rec):
    change_data(sites, "C:\\Users\\Ariel\\Desktop\\Lucy_AI_v2.0\\diccionary\\web.txt")
    task = rec.replace('abre', '').strip()
    if task in sites:
        for task in sites:
            if task in rec:
                sub.call(f'start chrome.exe {sites[task]}', shell=True)
                talk(f'Abriendo {task}')
    elif task in apps:
        for task in apps:
            if task in rec:
                talk(f'Abriendo {task}')
                os.startfile(apps[task])
    else:
        talk(f'No se ha encontrado el programa {task}')



def archivo(rec):
    change_data(files, "C:\\Users\\Ariel\\Desktop\\Lucy_AI_v2.0\\diccionary\\file.txt")
    file = rec.replace('archivo', '').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk(f'No se ha encontrado el archivo {file}')


# Función para obtener un chiste de Chuck Norris desde la API
def obtener_chiste_chuck_norris():
    url = 'https://api.chucknorris.io/jokes/random'
    
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            return data['value']
        else:
            return 'No se pudo obtener un chiste de Chuck Norris en este momento.'

    except Exception as e:
        return 'Hubo un error al intentar obtener un chiste de Chuck Norris.'

def chiste():
    chiste = obtener_chiste_chuck_norris()
    print("Lucy:", chiste)
    talk(chiste)