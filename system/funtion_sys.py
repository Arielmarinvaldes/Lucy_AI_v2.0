import keyboard
from pygame import mixer
from voices.voices import talk
import threading as tr
import datetime
import time
import os
import subprocess as sub
import requests
from motor.motor import listen

# Alarma
if not hasattr(time, 'clock'):
    time.clock = time.perf_counter


def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            talk("DESPIERTA!!!")
            mixer.init()
            mixer.music.load("sound\\Game-of-Thrones.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s" or 'stop' in rec == 'stop':
            mixer.music.stop()
            break


def thread_alarma(rec):
    t = tr.Thread(target=clock, args=(rec,))
    t.start()


# # abrir paginas web
# def abre(rec):
#     task = rec.replace('abre', '').strip()
#     if task in sites:
#         for task in sites:
#             if task in rec:
#                 sub.call(f'start chrome.exe {sites[task]}', shell=True)
#                 talk(f'Abriendo {task}')
#     elif task in apps:
#         for task in apps:
#             if task in rec:
#                 talk(f'Abriendo {task}')
#                 os.startfile(apps[task])
#     else:
#         talk(f'No se ha encontrado el programa {task}')


# De voz a texto
def escribe():
    try:
        with open(".\\diccionary\\nota.txt", 'a') as f:
            write(f)

    except FileNotFoundError as e:
        file = open("nota.txt", 'w')
        write(file)


def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen(".\\diccionary\\nota.txt", shell=True)


# Clima o Temperatura 
def return_weather(city):
    url = f"https://es.wttr.in/{city}?format=j1"

    response = requests.get(url)
    weather_dic = response.json()

    temp_c = weather_dic["current_condition"][0]['temp_C']
    desc_temp = weather_dic["current_condition"][0]['lang_es']
    desc_temp = desc_temp[0]['value']
    return temp_c, desc_temp


def clima():
    talk("De que pais o ciudad quiere saber el clima")
    city = listen()
    city = city.strip()
    temp_c, desc_temp = return_weather(city)
    # talk(f"La temperatura actual de {city} es {temp_c} grados célcius, y esta {desc_temp}.")
    print(f"La temperatura actual de {city} es {temp_c} °C. {desc_temp}.")


# Fecha y hora
def fecha(rec):
    fecha_actual = datetime.datetime.now()
    rec = rec.replace('qué', '').strip()
    if rec == 'hora':
        hour = fecha_actual.hour
        minute = fecha_actual.minute
        talk(f"Són las {hour} y {minute} minutos")

    elif 'dia es hoy':
        day = fecha_actual.day
        month = fecha_actual.strftime("%B")
        year = fecha_actual.year
        talk(f"La fecha actual es {day} de {month} de {year}.")
