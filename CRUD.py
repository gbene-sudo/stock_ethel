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
    rows = cursor.fetchall() #fetchall() devuelve todas las filas de la db

    barriles = []
    for row in rows:
        barril = Barril(id=row[0], tipo=row[1], capacidad=row[2], estado=row[3])
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

def filtro_por_tipo(barril_tipo): #Funcion para mostrar todos los barriles de un tipo (Rubia, Roja)
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(" SELECT * FROM barriles WHERE tipo LIKE ? ", (f"%{barril_tipo}%",))
    rows = cursor.fetchall() #fetchone() devuelve solo una fila

    barriles = []
    for row in rows:
        barril = Barril(id=row[0], tipo=row[1], capacidad=row[2], estado=row[3])
        barriles.append(barril)

    conn.close()
    return barriles

def filtro_por_litros(barril_capacidad): #Funcion para mostrar la info de una camada de barriles de la misma capacidad
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(" SELECT * FROM barriles WHERE capacidad LIKE ? ", (f"%{barril_capacidad}%",))
    rows = cursor.fetchall()  # fetchone() devuelve solo una fila

    barriles = []
    for row in rows:
        barril = Barril(id=row[0], tipo=row[1], capacidad=row[2], estado=row[3])
        barriles.append(barril)

    conn.close()
    return barriles

def filtro_por_estado(barril_estado):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(" SELECT * FROM barriles WHERE estado LIKE ? ", (f"%{barril_estado}%",))
    rows = cursor.fetchall()  # fetchone() devuelve solo una fila

    barriles = []
    for row in rows:
        barril = Barril(id=row[0], tipo=row[1], capacidad=row[2], estado=row[3])
        barriles.append(barril)

    conn.close()
    return barriles

