import os
from datetime import datetime

# Importamos desde la carpeta src
from src.database.db_manager import initialize_database, DATABASE_PATH # DATABASE_PATH para poder borrarla
from src.database import deudor_dao # Importamos el módulo DAO completo

def preparar_entorno_pruebas():
    """
    Prepara un entorno limpio para las pruebas:
    1. Borra la base de datos existente (si la hay).
    2. Inicializa una nueva base de datos con el schema.
    """
    print("--- Preparando Entorno de Pruebas ---")
    if os.path.exists(DATABASE_PATH):
        try:
            os.remove(DATABASE_PATH)
            print(f"Base de datos anterior eliminada: {DATABASE_PATH}")
        except Exception as e:
            print(f"No se pudo eliminar la base de datos anterior: {e}. Puede estar en uso.")
            print("Asegúrate de que ninguna otra aplicación esté usando el archivo .sqlite3.")
            return False # Indica que la preparación falló
            
    initialize_database() # Crea la estructura de tablas
    print("--- Entorno de Pruebas Listo --- \n")
    return True # Indica que la preparación fue exitosa

# --- PRUEBAS PARA agregar_deudor ---
def probar_agregar_deudor():
    print(">>> Iniciando pruebas para: agregar_deudor <<<")
    fecha_actual_iso = datetime.now().isoformat(sep=' ', timespec='seconds')
    
    # Caso 1: Agregar un deudor válido completo
    print("\nCaso 1: Agregando deudor válido completo...")
    id1 = deudor_dao.agregar_deudor(
        nom_deu="Juan Pérez Probador",
        fec_reg_deu=fecha_actual_iso,
        ced_deu="V10000001",
        tel_deu="0412-0001122",
        dir_deu="Calle de Prueba 123",
        est_deu='A'
    )
    if id1 is not None:
        print(f"  Resultado: ÉXITO. Deudor agregado con ID: {id1}")
    else:
        print(f"  Resultado: FALLO. No se pudo agregar el deudor.")
        assert id1 is not None, "Fallo Caso 1: agregar_deudor válido"


    # Caso 2: Agregar un deudor solo con campos obligatorios
    print("\nCaso 2: Agregando deudor con campos obligatorios...")
    id2 = deudor_dao.agregar_deudor(
        nom_deu="Ana Solitaria",
        fec_reg_deu=fecha_actual_iso
        # ced_deu, tel_deu, dir_deu son None por defecto en la función, est_deu es 'A'
    )
    if id2 is not None:
        print(f"  Resultado: ÉXITO. Deudor agregado con ID: {id2}")
    else:
        print(f"  Resultado: FALLO. No se pudo agregar el deudor.")
        assert id2 is not None, "Fallo Caso 2: agregar_deudor solo obligatorios"

    # Caso 3: Intentar agregar deudor con cédula duplicada (esperamos None)
    print("\nCaso 3: Intentando agregar deudor con cédula duplicada...")
    id3 = deudor_dao.agregar_deudor(
        nom_deu="Juan Pérez Duplicado",
        fec_reg_deu=fecha_actual_iso,
        ced_deu="V10000001" # Misma cédula que el primer deudor
    )
    if id3 is None:
        print(f"  Resultado: ÉXITO. No se agregó deudor con cédula duplicada (retornó None).")
    else:
        print(f"  Resultado: FALLO. Se agregó deudor con cédula duplicada (ID: {id3}).")
        assert id3 is None, "Fallo Caso 3: cédula duplicada permitió inserción"
    
    print(">>> Pruebas para agregar_deudor finalizadas <<<\n")
    return id1 # Retornamos un ID válido para usar en otras pruebas

# --- Bloque Principal de Ejecución de Pruebas ---
if __name__ == '__main__':
    if preparar_entorno_pruebas():
        # Ejecutamos las pruebas para cada función
        id_deudor_valido_para_otras_pruebas = probar_agregar_deudor()
        
        # Aquí iremos añadiendo llamadas a las otras funciones de prueba:
        # if id_deudor_valido_para_otras_pruebas:
        #     probar_obtener_deudor_por_id(id_deudor_valido_para_otras_pruebas)
        #     probar_actualizar_deudor(id_deudor_valido_para_otras_pruebas)
        #     probar_desactivar_deudor(id_deudor_valido_para_otras_pruebas)
        #     probar_reactivar_deudor(id_deudor_valido_para_otras_pruebas)

        # probar_listar_deudores_activos()
        # probar_listar_todos_los_deudores()
        # probar_obtener_deudor_por_cedula()

        print("\n--- Todas las pruebas planificadas han concluido ---")
        print(f"Recuerda revisar los mensajes de ÉXITO/FALLO y la base de datos '{DATABASE_PATH}' si es necesario.")
    else:
        print("No se pudo preparar el entorno de pruebas. Revisa los mensajes de error.")
        
        
        #Debes de agregar en la base de datos que los campos de cedula, numero de telefono y direccion del deudor sean obligatorios para que el caso 2 con campos obligatorios se cumpla, realiza todo esos cambios y dame los archivos actualizados que tengan esos cambios