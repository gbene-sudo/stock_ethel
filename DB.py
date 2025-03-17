import sqlite3 as sql

def conectar():
    return sql.connect("cerveceria.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
         CREATE TABLE IF NOT EXISTS barriles
          ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    capacidad REAL NOT NULL,
                    estado TEXT NOT NULL,
        )                                              
    """)

    conn.commit()
    conn.close()
