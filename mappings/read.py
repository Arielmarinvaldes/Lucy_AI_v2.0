# Rutas de archivos
WEB = "C:\\Users\\Ariel\\Desktop\\Lucy_AI_v2.0\\mappings\\web.txt"
APP = "C:\\Users\\Ariel\\Desktop\\Lucy_AI_v2.0\\mappings\\app.txt"
FILE = "C:\\Users\\Ariel\\Desktop\\Lucy_AI_v2.0\\mappings\\file.txt"
CONTACT = "C:\\Users\Ariel\Desktop\\Lucy_AI_v2.0\\mappings\\contact.txt"


# funcion para recorrer los archivos de los diccionarios
def change_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                key, val = line.strip().split(",")
                name_dict[key] = val

    except FileNotFoundError as e:
        print(e)


# Diccionarios
sites = dict()
change_data(sites, WEB)

files = dict()
change_data(files, FILE)

contact = dict()
change_data(contact, CONTACT)

apps = dict()
change_data(apps, APP)