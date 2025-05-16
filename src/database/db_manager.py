import sqlite3
import os

# Nombre del archivo de la base de datos.
# Se creará en la raíz del proyecto (SISTEMA_BODEGON/).
DATABASE_NAME = 'bodegon_data.sqlite3'

# Ruta al directorio raíz del proyecto (SISTEMA_BODEGON/)
# os.path.abspath(__file__) es la ruta al archivo actual (db_manager.py)
# os.path.dirname(...) sube un nivel en el directorio
# src/database/db_manager.py -> src/database/ -> src/ -> SISTEMA_BODEGON/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

# Ruta al archivo schema.sql, que está en el mismo directorio que este script
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')


def get_db_connection():
    """Crea y retorna una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre. ¡Muy útil!
        conn.execute("PRAGMA foreign_keys = ON;") # Crucial para mantener la integridad referencial.
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def initialize_database():
    """
    Inicializa la base de datos creando las tablas a partir del schema.sql.
    Se ejecuta para crear la estructura si la base de datos no existe o está vacía.
    """
    print(f"Intentando inicializar la base de datos en: {DATABASE_PATH}")
    print(f"Usando schema desde: {SCHEMA_PATH}")
    
    if not os.path.exists(SCHEMA_PATH):
        print(f"Error Crítico: No se encontró el archivo schema.sql en {SCHEMA_PATH}")
        return

    try:
        with get_db_connection() as conn: # Usar 'with' asegura que la conexión se cierre.
            if conn is None:
                print("No se pudo establecer conexión con la base de datos para inicializar.")
                return
            
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                schema_script = f.read()
            
            conn.executescript(schema_script) # executescript es para múltiples sentencias SQL.
            conn.commit() # Guarda los cambios.
            print(f"Base de datos inicializada/actualizada correctamente.")

    except sqlite3.Error as e:
        print(f"Error de SQLite al inicializar la base de datos: {e}")
    except FileNotFoundError: # Aunque ya lo verificamos, es buena práctica.
        print(f"Error: No se encontró el archivo schema.sql en {SCHEMA_PATH}")
    except Exception as e: # Captura cualquier otro error inesperado.
        print(f"Un error inesperado ocurrió durante la inicialización: {e}")

if __name__ == '__main__':
    # Esta sección se ejecuta solo si corres este archivo directamente con: python src/database/db_manager.py
    # Es útil para la configuración inicial de la base de datos.
    initialize_database()