"""
config_bd.py
------------
Propósito: leer las credenciales desde variables de entorno / archivo .env.
Así NO quedan contraseñas escritas en el código (recomendación 11 de la guía).
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()          # carga el archivo .env si existe
except ImportError:        # python-dotenv es opcional
    pass

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "mydb"),
    "charset": "utf8mb4",          # tildes y ñ correctas
}

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "mydb")
