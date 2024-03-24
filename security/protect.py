import os
import re
import hashlib
import random
import string
from voices.voices import talk


def verificar_len_password(password):
    if len(password) < 6:
        talk("Error: La contraseña debe tener al menos 6 caracteres.")
        return False
    # La contraseña pasa la verificaciones
    return True

def verificar_space_password(password):
    # Verifica si la contraseña consiste solo en espacios o puntos
    if password.isspace() or password == '.' * len(password):
        talk("Error: La contraseña no puede consistir solo en espacios o puntos.")
        return False
    # La contraseña pasa la verificaciones
    return True

def verificar_capital_password(password):
    # Verifica si la contraseña contiene al menos una mayúscula y al menos un número
    if not re.search(r"[A-Z]", password):
        talk("Error: La contraseña debe contener al menos una letra mayúscula.")
        return False
    # La contraseña pasa la verificaciones
    return True

def verificar_digit_password(password):
    if not re.search(r"\d", password):
        talk("Error: La contraseña debe contener al menos un número.")
        return False
    # La contraseña pasa la verificaciones
    return True

def verificar_illegal_character_password(password):
    # Verifica si la contraseña contiene caracteres no permitidos
    caracteres_no_permitidos = r"/()?¿&%$#@!¡¨{}[]+\-^`"
    if re.search(f"[{re.escape(caracteres_no_permitidos)}]", password):
        talk("  La contraseña contiene caracteres no permitidos.")
        return False

    # La contraseña pasa la verificaciones
    return True

def verificar_exist_password_regist(user, password, nombre, apellido):
    if not user or not password or not nombre or not apellido:
        talk("Error Por favor complete los campos vacíos.")
        return False
    return True
    
def verificar_exist_password_login(user, password):
    if not user or not password:
        talk("Error. Por favor complete ambos campos para iniciar seción.")
        return

# Función para hashear una contraseña y generar un salt
def hash_password(password):
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed_password, salt

# Función para verificar si la contraseña ingresada coincide con la almacenada como hash
def verificar_hash(password, hashed_password, salt):
    new_hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return new_hashed_password == hashed_password

def validar_correo_electronico(correo):
    expresion_regular = r"^(?!\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?<!\.)$"
    if re.match(expresion_regular, correo):
        return True
    else:
        if '.' not in correo:
            talk("Advertencia: Falta la extensión del dominio.")
        if correo.count('@') != 1:
            talk("Advertencia: El correo electrónico debe contener exactamente una '@'.")
        if correo.startswith('.') or correo.endswith('.'):
            talk("Advertencia: El correo electrónico no puede comenzar ni terminar con un punto.")
        if '..' in correo:
            talk("Advertencia: El correo electrónico no puede contener dos puntos consecutivos.")
        if '_@' in correo:
            talk("Advertencia: No se permite un guión bajo antes de '@'.")
        if '@.' in correo:
            talk("Advertencia: La posición del punto y la '@' no es válida.")
        return False

def validar_telefono_movil(numero):
    expresion_regular = r"^(?:(?:\+|00)([1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9])\d{1,14}|(?:\((?:00|\+)([1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9])\))\d{1,14}(?:\-?\d{1,8})?|(?:00|\+)([1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9])\d{1,14}(?:\-?\d{1,8})?|(?:\((?:00|\+)([1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9])\))\d{1,14})$"
    if re.match(expresion_regular, numero):
        return True
    else:
        talk("El numero de telefono es incorrecto.")
        return False
    
def generate_unique_token():
    # Genera un token aleatorio de 64 caracteres
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    # Generar un número de autorización aleatorio entre 1 y 999
    authorization_number = random.randint(1, 999)
    # Combinar el token y el número de autorización en un solo string
    unique_token = f"{token}_{authorization_number}"
    return unique_token