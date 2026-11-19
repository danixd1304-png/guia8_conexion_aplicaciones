"""
actividad2_crud.py
------------------
Guía 8 - Actividad 2: CRUD completo desde Python con consultas parametrizadas.
Tabla trabajada: Estudiante (base de datos mydb).

Usa el patrón DAO (Data Access Object): la clase EstudianteDAO concentra TODO el
acceso a la tabla; el menú solo pide datos y muestra resultados.

SEGURIDAD: ninguna consulta se arma concatenando texto. Los valores viajan
aparte en una tupla (%s) y el conector los escapa; por eso un texto como
    ' OR '1'='1
se trata como dato y no como código SQL.
"""
from datetime import datetime

import mysql.connector
from mysql.connector import Error

from config_bd import MYSQL_CONFIG

COLUMNAS = "idEstudiante, documento, nombres, apellidos, fecha_nacimiento, correo, telefono, direccion, id_carrera"


class EstudianteDAO:
    """Acceso a datos de la tabla Estudiante (CRUD)."""

    def _conectar(self):
        return mysql.connector.connect(**MYSQL_CONFIG)

    def _ejecutar(self, sql, params=()):
        """INSERT / UPDATE / DELETE: confirma (commit) o revierte (rollback)."""
        conexion = self._conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(sql, params)
            conexion.commit()
            return cursor.lastrowid or cursor.rowcount
        except Error:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def _consultar(self, sql, params=()):
        """SELECT: devuelve una lista de diccionarios."""
        conexion = self._conectar()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    # ---------------------------- CREATE ----------------------------
    def existe_documento(self, documento):
        # La columna documento no es UNIQUE en la tabla, así que se valida aquí.
        return bool(self._consultar("SELECT 1 FROM Estudiante WHERE documento = %s", (documento,)))

    def insertar(self, documento, nombres, apellidos, fecha_nac, correo, telefono, direccion, id_carrera):
        sql = ("INSERT INTO Estudiante (documento, nombres, apellidos, fecha_nacimiento, "
               "correo, telefono, direccion, id_carrera) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        return self._ejecutar(sql, (documento, nombres, apellidos, fecha_nac, correo, telefono, direccion, id_carrera))

    # ----------------------------- READ -----------------------------
    def listar(self, limite=20):
        return self._consultar(
            f"SELECT {COLUMNAS} FROM Estudiante ORDER BY idEstudiante DESC LIMIT %s", (limite,))

    def buscar(self, texto):
        """Busca por nombres, apellidos o documento. El comodín % se une al VALOR, no al SQL."""
        sql = (f"SELECT {COLUMNAS} FROM Estudiante "
               "WHERE nombres LIKE %s OR apellidos LIKE %s OR documento = %s ORDER BY idEstudiante")
        patron = f"%{texto}%"
        return self._consultar(sql, (patron, patron, texto))

    def obtener(self, id_estudiante):
        filas = self._consultar(f"SELECT {COLUMNAS} FROM Estudiante WHERE idEstudiante = %s", (id_estudiante,))
        return filas[0] if filas else None

    def carreras(self):
        return self._consultar("SELECT idCarrera, nombre FROM Carrera ORDER BY idCarrera")

    # ---------------------------- UPDATE ----------------------------
    def actualizar(self, id_estudiante, nombres, apellidos, correo, telefono, direccion):
        sql = ("UPDATE Estudiante SET nombres = %s, apellidos = %s, correo = %s, "
               "telefono = %s, direccion = %s WHERE idEstudiante = %s")
        return self._ejecutar(sql, (nombres, apellidos, correo, telefono, direccion, id_estudiante))

    # ---------------------------- DELETE ----------------------------
    def eliminar(self, id_estudiante):
        # Falla con IntegrityError si el estudiante tiene matrículas (FK sin cascada)
        return self._ejecutar("DELETE FROM Estudiante WHERE idEstudiante = %s", (id_estudiante,))


# ------------------------- Utilidades de consola -------------------------
def mostrar(filas):
    if not filas:
        print("  (sin resultados)")
        return
    print("\n  {:<4} {:<12} {:<12} {:<12} {:<28} {}".format(
        "ID", "DOCUMENTO", "NOMBRES", "APELLIDOS", "CORREO", "CARRERA"))
    print("  " + "-" * 82)
    for f in filas:
        print("  {:<4} {:<12} {:<12} {:<12} {:<28} {}".format(
            f["idEstudiante"], f["documento"], f["nombres"], f["apellidos"],
            f["correo"] or "-", f["id_carrera"] if f["id_carrera"] is not None else "-"))


def pedir_id():
    """Valida que el id sea un entero; evita errores y datos basura."""
    texto = input("  ID del estudiante: ").strip()
    if not texto.isdigit():
        print("  ID inválido: debe ser un número.")
        return None
    return int(texto)


def pedir_fecha():
    texto = input("  Fecha de nacimiento (AAAA-MM-DD, opcional): ").strip()
    if not texto:
        return None
    try:
        datetime.strptime(texto, "%Y-%m-%d")
        return texto
    except ValueError:
        print("  Fecha inválida; se guardará vacía.")
        return None


def menu():
    dao = EstudianteDAO()
    while True:
        print("\n===== GESTIÓN DE ESTUDIANTES (CRUD) =====")
        print("1. Insertar   2. Listar   3. Buscar   4. Actualizar   5. Eliminar   0. Salir")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                documento = input("  Documento: ").strip()
                nombres = input("  Nombres: ").strip()
                apellidos = input("  Apellidos: ").strip()
                if not documento or not nombres or not apellidos:
                    print("  Documento, nombres y apellidos son obligatorios.")
                    continue
                if dao.existe_documento(documento):
                    print("  Ya existe un estudiante con ese documento.")
                    continue
                fecha = pedir_fecha()
                correo = input("  Correo (opcional): ").strip() or None
                telefono = input("  Teléfono (opcional): ").strip() or None
                direccion = input("  Dirección (opcional): ").strip() or None
                print("  Carreras:", ", ".join(f"{c['idCarrera']}={c['nombre']}" for c in dao.carreras()[:8]), "...")
                id_carrera = input("  ID de carrera (opcional): ").strip()
                id_carrera = int(id_carrera) if id_carrera.isdigit() else None
                nuevo_id = dao.insertar(documento, nombres, apellidos, fecha, correo, telefono, direccion, id_carrera)
                print(f"  Estudiante creado con id {nuevo_id}.")
            elif opcion == "2":
                mostrar(dao.listar())
            elif opcion == "3":
                mostrar(dao.buscar(input("  Texto a buscar: ").strip()))
            elif opcion == "4":
                id_ = pedir_id()
                if id_ is None:
                    continue
                a = dao.obtener(id_)
                if not a:
                    print("  No existe un estudiante con ese id.")
                    continue
                print("  (Enter = dejar el valor actual)")
                nombres = input(f"  Nombres [{a['nombres']}]: ").strip() or a["nombres"]
                apellidos = input(f"  Apellidos [{a['apellidos']}]: ").strip() or a["apellidos"]
                correo = input(f"  Correo [{a['correo'] or ''}]: ").strip() or a["correo"]
                telefono = input(f"  Teléfono [{a['telefono'] or ''}]: ").strip() or a["telefono"]
                direccion = input(f"  Dirección [{a['direccion'] or ''}]: ").strip() or a["direccion"]
                dao.actualizar(id_, nombres, apellidos, correo, telefono, direccion)
                print("  Estudiante actualizado.")
            elif opcion == "5":
                id_ = pedir_id()
                if id_ is None:
                    continue
                if not dao.obtener(id_):
                    print("  No existe un estudiante con ese id.")
                    continue
                if input("  ¿Seguro que desea eliminarlo? (s/n): ").strip().lower() == "s":
                    dao.eliminar(id_)
                    print("  Estudiante eliminado.")
            elif opcion == "0":
                print("Hasta pronto.")
                break
            else:
                print("  Opción no válida.")
        except mysql.connector.IntegrityError as error:
            print("  No se pudo completar (restricción de integridad, p. ej. tiene matrículas o la carrera no existe):", error.msg)
        except Error as error:
            print("  Error de base de datos:", error)


if __name__ == "__main__":
    menu()
