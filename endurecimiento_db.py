import sqlite3
import os
from datetime import datetime

# Archivos de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_ORIGINAL = os.path.join(BASE_DIR, "usuarios.db")
DB_RESPALDO = os.path.join(BASE_DIR, "usuarios_respaldo.db")


def endurecer_base_datos():
    print("=" * 58)
    print("     ENDURECIMIENTO DE BASE DE DATOS SQLITE")
    print("     Materia: Seguridad Informatica")
    print("=" * 58)

    if not os.path.exists(DB_ORIGINAL):
        print("ERROR: No se encontro el archivo usuarios.db.")
        print("Ejecuta primero las aplicaciones del proyecto.")
        return

    try:
        # Crear una copia consistente de la base de datos
        with sqlite3.connect(DB_ORIGINAL) as origen:
            with sqlite3.connect(DB_RESPALDO) as respaldo:
                origen.backup(respaldo)

        print("\n[OK] Copia de seguridad creada.")
        print(f"Archivo: {os.path.basename(DB_RESPALDO)}")

        # Aplicar configuraciones y revisar la base de datos
        with sqlite3.connect(DB_ORIGINAL, timeout=10) as conexion:
            conexion.execute("PRAGMA busy_timeout = 5000")
            conexion.execute("PRAGMA secure_delete = ON")
            conexion.execute("PRAGMA trusted_schema = OFF")

            # Comprobar la integridad de SQLite
            resultado = conexion.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]

            print("\nComprobacion de integridad:")
            print(f"Resultado: {resultado}")

            # Consultar las tablas existentes
            tablas = conexion.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """).fetchall()

            print("\nTablas encontradas:")
            if tablas:
                for tabla in tablas:
                    print(f"- {tabla[0]}")
            else:
                print("No se encontraron tablas.")

            # Revisar las columnas de la tabla usuarios
            existe_usuarios = any(
                tabla[0] == "usuarios" for tabla in tablas
            )

            if existe_usuarios:
                columnas = conexion.execute(
                    "PRAGMA table_info(usuarios)"
                ).fetchall()

                print("\nEstructura de la tabla usuarios:")
                for columna in columnas:
                    print(f"- {columna[1]}")

        print("\nRESUMEN")
        print("- Copia de seguridad: creada")
        print("- Integridad:", resultado)
        print("- Tiempo de espera de conexiones: configurado")
        print("- Borrado seguro de registros: activado")
        print("- Configuracion de esquema confiable: desactivada")
        print("\nFecha:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("=" * 58)
        print("Revision finalizada.")

        if resultado != "ok":
            print("ADVERTENCIA: revisa el estado de la base de datos.")

    except sqlite3.Error as error:
        print(f"\nError de SQLite: {error}")
    except OSError as error:
        print(f"\nError al trabajar con los archivos: {error}")


if __name__ == "__main__":
    endurecer_base_datos()
