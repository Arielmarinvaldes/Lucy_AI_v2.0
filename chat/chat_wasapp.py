import pyautogui as at
import time
import webbrowser

from mappings.read import change_data, contact
from motor.motor import listen
from voices.voices import talk


def send_message(contact, message):
    webbrowser.open(f"https://web.whatsapp.com/send?phone={contact}&text={message}")
    time.sleep(15)
    at.press("enter")
    print({message})


def envia_mensaje(rec):
    change_data(contact, "C:\\Users\Ariel\Desktop\\Lucy_AI_v2.0\\diccionary\\contact.txt")
    talk("¿A quién quieres enviar el mensaje?")
    contacts = listen()
    contacts = contacts.strip().capitalize()

    if contacts in contact:
        for cont in contact:
            if cont == contacts:
                contacts = contact[cont]
                talk("Que mensaje quieres enviar")
                message = listen()
                talk("Enviando mensaje...")
                send_message(contacts, message)
    else:
        talk(f"No has agregado {contacts} a tu lista de contactos")
