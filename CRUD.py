from DB import conectar
from models import Barril

def crear_barril():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(""""
        INSERT INTO barriles (tipo,estado,capacidad) VALUES (?,?,?)
    """), (Barril.tipo, Barril.estado, Barril.capacidad)

    conn.commit()
    conn.close()


    ''' Si te interesa devolver la id
    conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    '''

