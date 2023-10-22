
from googlesearch import search


# Función para buscar en la web
def search_web(query):
    try:
        results = list(search(query, num=5, lang="es"))
        if results:
            print("Aquí están los resultados de la búsqueda:")
            for i, result in enumerate(results):
                print(f"{i + 1}. {result}")
        else:
            print("Lo siento, no encontré resultados para esa búsqueda.")
    except Exception as e:
        print("Hubo un error al realizar la búsqueda en la web.")


search_web("hola")