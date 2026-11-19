"""
actividad1_conexion.py
----------------------
Guía 8 - Actividad 1: conexión básica Python-MySQL (base de datos mydb).

Los 5 pasos de una operación con MySQL Connector:
    1. Instalar el conector  (pip install mysql-connector-python)
    2. Conectar              (mysql.connector.connect)
    3. Crear el cursor       (conexion.cursor)
    4. Ejecutar la consulta  (cursor.execute)
    5. Cerrar cursor y conexión (finally)
"""
import mysql.connector
from mysql.connector import Error

from config_bd import MYSQL_CONFIG


def main():
    conexion = None
    cursor = None
    try:
        # Paso 2: abrir la conexión
        conexion = mysql.connector.connect(**MYSQL_CONFIG)
        if conexion.is_connected():
            print("Conexión exitosa a MySQL, versión:", conexion.server_info)
            print("Base de datos:", MYSQL_CONFIG["database"])

        # Paso 3: crear el cursor
        cursor = conexion.cursor()

        # Paso 4: SELECT con JOIN (sin datos del usuario, por eso sin parámetros)
        cursor.execute(
            "SELECT e.idEstudiante, e.documento, e.nombres, e.apellidos, c.nombre "
            "FROM Estudiante e LEFT JOIN Carrera c ON c.idCarrera = e.id_carrera "
            "ORDER BY e.idEstudiante LIMIT 10"
        )
        filas = cursor.fetchall()

        print("\n{:<4} {:<12} {:<12} {:<12} {}".format("ID", "DOCUMENTO", "NOMBRES", "APELLIDOS", "CARRERA"))
        print("-" * 72)
        for id_, documento, nombres, apellidos, carrera in filas:
            print("{:<4} {:<12} {:<12} {:<12} {}".format(id_, documento, nombres, apellidos, carrera or "(sin carrera)"))

        cursor.execute("SELECT COUNT(*) FROM Estudiante")
        print(f"\nMostrando {len(filas)} de {cursor.fetchone()[0]} estudiantes.")

    except Error as error:
        # Manejo de errores: contraseña incorrecta, BD inexistente, servidor apagado...
        print("ERROR de MySQL:", error)

    finally:
        # Paso 5: cerrar siempre, haya o no error (evita fugas de conexiones)
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")


if __name__ == "__main__":
    main()
