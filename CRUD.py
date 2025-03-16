from DB import conectar
from models import Barril

def crear_barril():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(""""
        INSERT INTO barriles (PRIMARY KEY id,tipo,estado,capacidad) VALUES (?,?,?)
    """), (barril.tipo, barril.tipo, barril.estado, barril.capacidad)
    conn.commit()
    conn.close()

