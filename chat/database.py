import sqlite3


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("chat/Brain.db")
        print("La conexión a la base de datos se ha establecido correctamente.")
    except Error as e:
        print(e)
    return conn


def get_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM preguntasyrespuestas")
    return cursor.fetchall()

bot_list = list()


def get_questionanswers():
    rows = get_table()
    bot_list = [(row[0], row[1]) for row in rows]
    return bot_list
