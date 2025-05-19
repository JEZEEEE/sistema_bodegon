import sqlite3
from .db_manager import get_db_connection # Importamos la función de conexión

# usar datetime para las fechas en futuras funciones,
#  from datetime import datetime

def agregar_deudor(nom_deu, fec_reg_deu, ced_deu=None, tel_deu=None, dir_deu=None, est_deu='A'):
    """
    Agrega un nuevo deudor a la tabla Deudores.
    Retorna el ID del nuevo deudor (ide_deu) si fue exitoso, None en caso de error.
    """
    sql = """
        INSERT INTO Deudores (nom_deu, ced_deu, tel_deu, dir_deu, fec_reg_deu, est_deu)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        with get_db_connection() as conn:
            if conn is None: return None
            cursor = conn.cursor()
            cursor.execute(sql, (nom_deu, ced_deu, tel_deu, dir_deu, fec_reg_deu, est_deu))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError: # Ej: Cédula duplicada
        return None 
    except sqlite3.Error:
        return None

def listar_deudores_activos():
    """
    Retorna una lista de diccionarios, cada uno representando un deudor activo.
    Ordenados por nombre. Retorna lista vacía si no hay o en caso de error.
    """
    sql = """
        SELECT ide_deu, nom_deu, ced_deu, tel_deu, dir_deu, fec_reg_deu, est_deu
        FROM Deudores
        WHERE est_deu = 'A'
        ORDER BY nom_deu ASC
    """
    deudores = []
    try:
        with get_db_connection() as conn:
            if conn is None: return deudores
            cursor = conn.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                deudores.append(dict(row))
        return deudores
    except sqlite3.Error:
        return deudores

def listar_todos_los_deudores():
    """
    Retorna una lista de diccionarios con todos los deudores (activos e inactivos).
    Ordenados por nombre. Retorna lista vacía si no hay o en caso de error.
    """
    sql = """
        SELECT ide_deu, nom_deu, ced_deu, tel_deu, dir_deu, fec_reg_deu, est_deu
        FROM Deudores
        ORDER BY nom_deu ASC
    """
    deudores = []
    try:
        with get_db_connection() as conn:
            if conn is None: return deudores
            cursor = conn.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                deudores.append(dict(row))
        return deudores
    except sqlite3.Error:
        return deudores

def obtener_deudor_por_id(ide_deu):
    """
    Retorna un diccionario con los datos del deudor correspondiente al ide_deu.
    Retorna None si no se encuentra o en caso de error.
    """
    sql = """
        SELECT ide_deu, nom_deu, ced_deu, tel_deu, dir_deu, fec_reg_deu, est_deu
        FROM Deudores
        WHERE ide_deu = ?
    """
    try:
        with get_db_connection() as conn:
            if conn is None: return None
            cursor = conn.cursor()
            cursor.execute(sql, (ide_deu,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error:
        return None

def obtener_deudor_por_cedula(ced_deu):
    """
    Retorna un diccionario con los datos del deudor correspondiente a la ced_deu.
    Retorna None si no se encuentra o en caso de error.
    """
    sql = """
        SELECT ide_deu, nom_deu, ced_deu, tel_deu, dir_deu, fec_reg_deu, est_deu
        FROM Deudores
        WHERE ced_deu = ?
    """
    try:
        with get_db_connection() as conn:
            if conn is None: return None
            cursor = conn.cursor()
            cursor.execute(sql, (ced_deu,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error:
        return None

def actualizar_deudor(ide_deu, nom_deu, ced_deu, tel_deu, dir_deu, est_deu):
    """
    Actualiza los datos de un deudor existente identificado por su ide_deu.
    La fecha de registro (fec_reg_deu) no se actualiza.
    Retorna True si la actualización fue exitosa (al menos una fila afectada), False en caso contrario.
    """
    sql = """
        UPDATE Deudores
        SET nom_deu = ?, 
            ced_deu = ?, 
            tel_deu = ?, 
            dir_deu = ?, 
            est_deu = ?
        WHERE ide_deu = ?
    """
    try:
        with get_db_connection() as conn:
            if conn is None: return False
            cursor = conn.cursor()
            cursor.execute(sql, (nom_deu, ced_deu, tel_deu, dir_deu, est_deu, ide_deu))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.IntegrityError: # Ej: Cédula duplicada
        return False
    except sqlite3.Error:
        return False

def desactivar_deudor(ide_deu):
    """
    Desactiva un deudor (est_deu = 'I') identificado por su ide_deu.
    Solo desactiva si actualmente está activo.
    Retorna True si la desactivación fue exitosa (al menos una fila afectada), False en caso contrario.
    """
    sql = """
        UPDATE Deudores
        SET est_deu = 'I'
        WHERE ide_deu = ? AND est_deu = 'A'
    """
    try:
        with get_db_connection() as conn:
            if conn is None: return False
            cursor = conn.cursor()
            cursor.execute(sql, (ide_deu,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error:
        return False

def reactivar_deudor(ide_deu):
    """
    Reactiva un deudor (est_deu = 'A') identificado por su ide_deu.
    Solo reactiva si actualmente está inactivo.
    Retorna True si la reactivación fue exitosa (al menos una fila afectada), False en caso contrario.
    """
    sql = """
        UPDATE Deudores
        SET est_deu = 'A'
        WHERE ide_deu = ? AND est_deu = 'I'
    """
    try:
        with get_db_connection() as conn:
            if conn is None: return False
            cursor = conn.cursor()
            cursor.execute(sql, (ide_deu,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error:
        return False