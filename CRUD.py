from DB import conectar
from models import Barril

def crear_barril():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(""""
        INSERT INTO barriles (tipo,estado,capacidad)
            VALUES (?,?,?)
    """), (Barril.tipo, Barril.estado, Barril.capacidad)

    conn.commit()
    conn.close()
    ''' Si te interesa devolver la id
    conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    '''

def obtener_barriles():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(" SELECT * FROM barriles ")
    rows = cursor.fetchall()

    barriles = []
    for row in rows:
        barril = Barril(id=row[0],capacidad=row[1],estado=row[2],tipo=row[3])
        barriles.append(barril)

    conn.close()
    return barriles

def actualizar_barril(barril_id, nuevo_estado):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(" UPDATE barriles SET estado = ? WHERE id = ? ", (nuevo_estado, barril_id))

    conn.commit()
    conn.close()

def borrar_barril(barril_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(" DELETE FROM barriles WHERE id=? ", (barril_id,))

    conn.commit()
    conn.close()



