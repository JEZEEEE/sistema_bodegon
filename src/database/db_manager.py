import sqlite3
import os

DATABASE_NAME = 'bodegon_data.sqlite3'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')

def get_db_connection():
    """Crea y retorna una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def initialize_database():
    """Inicializa la BD creando las tablas a partir del schema.sql."""
    print(f"Intentando inicializar la base de datos en: {DATABASE_PATH}")
    print(f"Usando schema desde: {SCHEMA_PATH}")
    
    if not os.path.exists(SCHEMA_PATH):
        print(f"Error Crítico: No se encontró el archivo schema.sql en {SCHEMA_PATH}")
        return

    try:
        with get_db_connection() as conn:
            if conn is None:
                print("No se pudo establecer conexión con la base de datos para inicializar.")
                return
            
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                schema_script = f.read()
            
            conn.executescript(schema_script)
            conn.commit()
            print(f"Base de datos inicializada/actualizada correctamente.")
    except sqlite3.Error as e:
        print(f"Error de SQLite al inicializar la base de datos: {e}")
    except Exception as e:
        print(f"Un error inesperado ocurrió durante la inicialización: {e}")

if __name__ == '__main__':
    initialize_database() # Este script ahora solo se usa para inicializar la BD.
    
    
    