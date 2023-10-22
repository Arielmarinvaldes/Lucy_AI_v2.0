import wikipedia
import pywhatkit
from voices.voices import talk
import subprocess as sub
import os


# funcion para recorrer los archivos de los diccionarios
def change_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",")
                val = val.rstrip("\n")
                name_dict[key] = val

    except FileNotFoundError as e:
        print(e)

# # diccionarios
# sites = dict()
# change_data(sites, "web.txt")

# files = dict()
# change_data(files, "file.txt")

# contact = dict()
# change_data(contact, "contact.txt")

# apps = dict()
# change_data(apps, "app.txt")


def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 1)
    talk(wiki)
    write_text(search + ": " + wiki)


def reproduce(rec):
    music = rec.replace('reproduce', '')
    talk(f"Reproduciendo {music}")
    pywhatkit.playonyt(music)


def abre(rec):
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
    file = rec.replace('archivo', '').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk(f'No se ha encontrado el archivo {file}')
