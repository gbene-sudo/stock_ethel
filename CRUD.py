from DB import conectar
from models import Barril

def crear_barril(tipo,capacidad,estado): #Creacion de un barril
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO barriles (tipo,capacidad,estado)
            VALUES (?,?,?)
    """, (tipo, capacidad, estado))

    conn.commit()
    conn.close()
    ''' Si te interesa devolver la id
    conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    '''

def obtener_barriles(): #Mostrar todos los barriles
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

def actualizar_barril(barril_id, tipo_barril, nuevo_estado, nuevo_capacidad): #Actualizar los datos de un barril, pidiendole los nuevos
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(" UPDATE barriles SET tipo = ? WHERE id = ? ", (tipo_barril, barril_id))
    cursor.execute(" UPDATE barriles SET capacidad = ? WHERE id = ? ", (nuevo_capacidad, barril_id))
    cursor.execute(" UPDATE barriles SET estado = ? WHERE id = ? ", (nuevo_estado, barril_id))

    conn.commit()
    conn.close()

def borrar_barril(barril_id): #Borrar un barril usando la id como parametro
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(" DELETE FROM barriles WHERE id=? ", (barril_id,))

    conn.commit()
    conn.close()

#FILTROS
def filtro_por_tipo(orden="ASC"): #Funcion para filtrar por orden la lista segun el tipo
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f" SELECT * FROM barriles ORDER BY tipo {orden}")
    rows = cursor.fetchall()

    barriles = []
    for row in rows:
        barril = Barril(id=row[0], tipo=row[1], capacidad=row[2], estado=row[3])
        barriles.append(barril)

    conn.close()
    return barriles

def filtro_por_litros(orden="ASC"): #Funcion para filtrar por orden la lista segun la capacidad
    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(f"""
            SELECT * FROM barriles 
            ORDER BY 
                CASE capacidad
                    WHEN '50' THEN 1
                    WHEN '30' THEN 2
                    WHEN '20' THEN 3
                    WHEN '15' THEN 4
                    WHEN '10' THEN 5
                END {orden}
        """)
    rows = cursor.fetchall()  # fetchone() devuelve solo una fila

    barriles = []
    for row in rows:
        barril = Barril(id=row[0], tipo=row[1], capacidad=row[2], estado=row[3])
        barriles.append(barril)

    conn.close()
    return barriles

def filtro_por_estado(orden="ASC"): #Funcion para filtrar por orden la lista segun el estado
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM barriles 
        ORDER BY 
            CASE estado
                WHEN 'Lleno' THEN 1
                WHEN 'Entregado' THEN 2
                WHEN 'Latas' THEN 3
                WHEN 'Bar' THEN 4
                WHEN 'Incompleto' THEN 5
                WHEN 'Vacio' THEN 6
            END {orden}
    """)
    rows = cursor.fetchall()  # fetchone() devuelve solo una fila

    barriles = []
    for row in rows:
        barril = Barril(id=row[0], tipo=row[1], capacidad=row[2], estado=row[3])
        barriles.append(barril)

    conn.close()
    return barriles

def order_by_id(orden="ASC"): #Funcion para filtrar por orden la lista segun la id
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM barriles ORDER BY id {orden}")
    rows = cursor.fetchall()  # fetchone() devuelve solo una fila

    barriles = []
    for row in rows:
        barril = Barril(id=row[0], tipo=row[1], capacidad=row[2], estado=row[3])
        barriles.append(barril)

    conn.close()
    return barriles

def filtro_por_id(barril_id): #Funcion para mostrar la info de un solo barril usando la id como parametro
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(" SELECT * FROM barriles WHERE id = ? ", (barril_id,))
    row = cursor.fetchone()  # fetchone() devuelve solo una fila

    conn.close()
    if row:
        return Barril(id=row[0], tipo=row[1], capacidad=row[2], estado=row[3])
    else:
        return None

