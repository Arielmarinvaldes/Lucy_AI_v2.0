import os
import sqlite3
from aifc import Error


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("db/Brain.db")
        print("La conexión a la base de datos se ha establecido correctamente.")
    except Error as e:
        print(e)
    return conn


def get_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM preguntasyrespuestas")
    rows = cursor.fetchall()
    connection.close()  # Cerrar la conexión antes de realizar cambios en el sistema de archivos
    return rows


def hide_database_files():
    # Mover los archivos a un directorio oculto después de cerrar la conexión
    os.rename("db/Brain.db-wal", ".Brain.db-wal")
    os.rename("db/Brain.db", ".Brain.db")
    os.rename("db/Brain.db-shm", ".Brain.db-shm")
    os.rename("db/sqlite3", ".sqlite3")


bot_list = list()


def get_questionanswers():
    rows = get_table()
    bot_list = [(row[0], row[1]) for row in rows]
    return bot_list
