import keyboard
from pygame import mixer
from voices.voices import talk
import threading as tr
import datetime
import time

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
            mixer.music.load("sonido\\Game-of-Thrones.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s" or 'stop' in rec == 'stop':
            mixer.music.stop()
            break


def thread_alarma(rec):
    t = tr.Thread(target=clock, args=(rec,))
    t.start()