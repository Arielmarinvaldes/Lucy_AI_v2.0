import os
import re
import hashlib
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


