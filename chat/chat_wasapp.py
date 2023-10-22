import webbrowser
import pyautogui as at
import time
from voices.voices import talk
from motor.motor import listen

# funcion para recorrer los archivos de los diccionarios
def change_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                key, val = line.strip().split(",")
                name_dict[key] = val

    except FileNotFoundError as e:
        print(e)


contact = dict()
change_data(contact, "contact.txt")

def send_message(contact, message):
    webbrowser.open(f"https://web.whatsapp.com/send?phone={contact}&text={message}")
    time.sleep(15)
    at.press("enter")
    print({message})


def envia_mensaje(rec):
    talk("¿A quién quieres enviar el mensaje?")
    contacts = listen()
    contacts = contacts.strip().capitalize()

    if contacts in cd.contact:
        for cont in contact:
            if cont == contacts:
                contacts = contact[cont]
                talk("Que mensaje quieres enviar")
                message = listen()
                talk("Enviando mensaje...")
                send_message(contacts, message)
    else:
        talk(f"No has agregado {contacts} a tu lista de contactos")
