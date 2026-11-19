"""
actividad3_procedimientos.py
----------------------------
Guía 8 - Actividad 3: llamar procedimientos almacenados con callproc() y
capturar los parámetros OUT (base de datos mydb).

Procedimientos:
    RegistrarMatricula(IN id_estudiante, IN id_curso, OUT mensaje)   <- Práctica 5
    sp_promedio_estudiante(IN id_estudiante, OUT promedio)           <- adicional
    sp_historial_estudiante(IN id_estudiante)  (devuelve un SELECT)  <- adicional

callproc(nombre, [args]) devuelve la lista de argumentos ya modificada: en la
posición de cada parámetro OUT viene el valor que calculó el procedimiento.
Si el procedimiento hace un SELECT, ese resultado se lee con stored_results().
"""
import mysql.connector
from mysql.connector import Error

from config_bd import MYSQL_CONFIG


def registrar_matricula(conexion, cursor, id_estudiante, id_curso):
    # Argumentos: [IN, IN, OUT]. Para el OUT se envía un valor inicial ("").
    resultado = cursor.callproc("RegistrarMatricula", [id_estudiante, id_curso, ""])
    conexion.commit()              # el SP hace INSERT: se confirma la transacción
    return resultado[2]            # posición del parámetro OUT (mensaje)


def promedio_estudiante(cursor, id_estudiante):
    resultado = cursor.callproc("sp_promedio_estudiante", [id_estudiante, 0])
    return resultado[1]            # OUT: promedio (None si no tiene notas)


def historial_estudiante(cursor, id_estudiante):
    cursor.callproc("sp_historial_estudiante", [id_estudiante])
    filas = []
    for resultset in cursor.stored_results():     # conjuntos de resultados del SP
        filas.extend(resultset.fetchall())
    return filas


def contar_matriculas(cursor, id_estudiante):
    # Consulta parametrizada de apoyo para comprobar el efecto del procedimiento
    cursor.execute("SELECT COUNT(*) FROM Matricula WHERE id_estudiante = %s", (id_estudiante,))
    return cursor.fetchone()[0]


def main():
    conexion = None
    cursor = None
    try:
        conexion = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conexion.cursor()

        print("=== 1. RegistrarMatricula (Práctica 5): parámetro OUT con el mensaje ===")
        print("Matrículas del estudiante 1 antes:", contar_matriculas(cursor, 1))
        print("Caso válido    (estudiante 1, curso 1)  ->", registrar_matricula(conexion, cursor, 1, 1))
        print("Curso inexistente (estudiante 1, curso 999) ->", registrar_matricula(conexion, cursor, 1, 999))
        print("Estudiante inexistente (999, curso 1)       ->", registrar_matricula(conexion, cursor, 999, 1))
        print("Matrículas del estudiante 1 después:", contar_matriculas(cursor, 1))

        print("\n=== 2. sp_promedio_estudiante: parámetro OUT numérico ===")
        for id_est in (1, 2, 31):
            print(f"Promedio del estudiante {id_est}:", promedio_estudiante(cursor, id_est))

        print("\n=== 3. sp_historial_estudiante: SELECT dentro del procedimiento ===")
        for periodo, curso, creditos, nota in historial_estudiante(cursor, 1):
            print(f"  {periodo} | {curso:<35} | {creditos} créditos | nota: {nota if nota is not None else 'sin nota'}")

    except Error as error:
        print("ERROR de MySQL:", error)
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
            print("\nConexión cerrada.")


if __name__ == "__main__":
    main()
