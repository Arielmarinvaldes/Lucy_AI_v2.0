# test 1
def valoresEstadisticos(f):
    minimo_impar = float('inf')
    maximo_impar = float('-inf')
    suma_valores = 0
    cantidad_valores  = 0
    max_number = None
    count_max_number = 0

    for num in f:
        # Verificar si el número es impar
        if num % 2 != 0:

            if num < minimo_impar:
                minimo_impar = num

            if num > maximo_impar:
                maximo_impar = num

            suma_valores += num
            cantidad_valores += 1

        if max_number is None or num > max_number:
            max_number = num
            count_max_number = 1

        elif num == max_number:
            count_max_number += 1
    print(f"El número más grande es:({max_number}) y aparece {count_max_number} veces")

    if cantidad_valores > 0:
        media_valores = suma_valores / cantidad_valores
        print("La media arictmética es:", media_valores)

    if minimo_impar != float('inf'):
        print("El mínimo valor impar es:", minimo_impar)
        print("El máximo valor impar es:", maximo_impar)
    else:
        print("No hay valores impares en este fichero")


file = [3, 8, 9, 2, 10, 8, 5, 10, 2, 1, 8]
valoresEstadisticos(file)


# Test 2
def comprobarPalindromo(f):
    word = f.lower()
    if word == word[::-1]:
        print(f"La palabra ({word}),es un Palíndromo y tiene ({len(word)}) letras")
    else:
        print(f"{word},no es un Palíndromo")

file = "Radar"
comprobarPalindromo(file)

#test 3
def dar_subcadena(text, inicio, num_letras):
    # Implementación de la función dar_subcadena
    return text[inicio:inicio + num_letras]


def is_Vocal(letra):
    # Verifica si la ultima letra de la palabra es una vocal
    return letra.lower() in "aeiou"


def traducir_palabra(word, idioma):
    # Defino estas variables por si queremos cambiar de palabras, agilizamos el proceso
    ejemp1 = "ujem"
    ejemp2 = "kov"

    # Identifica el idioma
    if idioma == 1:  # Alemán
        # Obtiene la ultima letra de la palabra 
        ultima_letra = word[-1]

        # Verifica si la última letra es vocal
        if is_Vocal(ultima_letra):
            # Quitar la vocal y añade "ujem"
            traduccion = word[:-1] + ejemp1
            print(f"{word}-> {traduccion}")
        else:
            # Quita 2 letras y añade "ujem"
            traduccion = dar_subcadena(word, 0, len(word) - 2) + ejemp1
            print(f"{word}-> {traduccion}")
    elif idioma == 2:  # Búlgaro
        # Obtiene la ultima letra de la palabra 
        ultima_letra = word[-1]

        # Verifica si la última letra es vocal
        if is_Vocal(ultima_letra):
            # Añade "kov"
            traduccion = word + ejemp2
            print(f"{word}-> {traduccion}")
        else:
            # Quita 1 letra y añade "kov"
            traduccion = dar_subcadena(word, 0, len(word) - 1) + ejemp2
            print(f"{word}-> {traduccion}")
    else:
        print("Idioma no válido, prueba con:(1 es Aleman o 2 es Búlgaro)")


traducir_palabra("silla", 1)
traducir_palabra("camión", 1)
traducir_palabra("silla", 2)
traducir_palabra("camión", 2)
