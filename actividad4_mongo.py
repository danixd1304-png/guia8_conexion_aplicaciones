"""
actividad4_mongo.py
-------------------
Guía 8 - Actividad 4: conexión a MongoDB Atlas desde Python (pymongo) y CRUD básico:
insert_one, find, update_one, delete_one.

Se guarda en MongoDB el perfil de un estudiante de la base relacional mydb
(datos flexibles: intereses y preferencias). La cadena de conexión (MONGO_URI)
se lee del archivo .env; no se escribe en el código. En Atlas: permitir tu IP en
Network Access y crear un usuario en Database Access.
"""
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config_bd import MONGO_DB, MONGO_URI


def conectar():
    # serverSelectionTimeoutMS: no esperar indefinidamente si Atlas no responde
    cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    cliente.admin.command("ping")          # verifica la conexión de verdad
    return cliente


def main():
    cliente = None
    try:
        cliente = conectar()
        print("Conexión exitosa a MongoDB. Bases disponibles:", cliente.list_database_names())
        coleccion = cliente[MONGO_DB]["perfiles_estudiantes"]

        # ---------------- CREATE: insert_one ----------------
        documento = {
            "documento": "1001234567",          # mismo documento que en MySQL (Estudiante 1)
            "nombres": "Juan",
            "apellidos": "García",
            "intereses": ["bases de datos", "python"],
            "preferencias": {"tema": "oscuro", "idioma": "es"},
            "creado_en": datetime.now(timezone.utc),
        }
        resultado = coleccion.insert_one(documento)
        print("\n[insert_one] _id insertado:", resultado.inserted_id)

        # ---------------- READ: find ----------------
        print("\n[find] todos los perfiles:")
        for doc in coleccion.find({}, {"_id": 0, "creado_en": 0}):
            print("  ", doc)

        # El filtro usa str() para que un atacante no pueda enviar un objeto
        # como {"$ne": ""} y alterar la consulta (inyección NoSQL).
        filtro = {"documento": str("1001234567")}
        print("\n[find_one] perfil con documento 1001234567:", coleccion.find_one(filtro, {"_id": 0, "creado_en": 0}))

        # ---------------- UPDATE: update_one ----------------
        resultado = coleccion.update_one(
            filtro,
            {"$set": {"preferencias.tema": "claro"}, "$push": {"intereses": "mongodb"}},
        )
        print("\n[update_one] encontrados:", resultado.matched_count, "| modificados:", resultado.modified_count)
        print("  Después:", coleccion.find_one(filtro, {"_id": 0, "creado_en": 0}))

        # ---------------- DELETE: delete_one ----------------
        resultado = coleccion.delete_one(filtro)
        print("\n[delete_one] eliminados:", resultado.deleted_count)
        print("  Documentos restantes:", coleccion.count_documents({}))

    except PyMongoError as error:
        print("ERROR de MongoDB:", error)
    finally:
        if cliente is not None:
            cliente.close()
            print("\nConexión cerrada.")


if __name__ == "__main__":
    main()
