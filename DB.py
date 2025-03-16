import sqlite3 as sql

def conectar():
    conn = sql.connect("barriles.db")
    return conn

