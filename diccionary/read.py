# funcion para recorrer los archivos de los diccionarios
def change_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                key, val = line.strip().split(",")
                name_dict[key] = val

    except FileNotFoundError as e:
        print(e)

# Rutas de archivo completas a los archivos de diccionario
WEB = "C:\\Users\\amval\\OneDrive\\Escritorio\\whisper-python-assistant-main\\diccionary\\web.txt"
FILE = "C:\\Users\\amval\\OneDrive\\Escritorio\\whisper-python-assistant-main\\diccionary\\file.txt"
CONTACT = "C:\\Users\\amval\\OneDrive\\Escritorio\\whisper-python-assistant-main\\diccionary\\contact.txt"
APP = "C:\\Users\\amval\\OneDrive\\Escritorio\\whisper-python-assistant-main\\diccionary\\app.txt"

# Diccionarios
sites = dict()
change_data(sites, WEB)

files = dict()
change_data(files, FILE)

contact = dict()
change_data(contact, CONTACT)

apps = dict()
change_data(apps, APP)