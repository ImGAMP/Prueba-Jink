import os
from dotenv import load_dotenv
from pymongo import MongoClient
import ssl

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "inventario_db")

# Configuración segura para producción y desarrollo
client = MongoClient(
    MONGO_URI,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,  # Para desarrollo/testing
    connectTimeoutMS=5000,
    socketTimeoutMS=30000,
    serverSelectionTimeoutMS=5000
)

db = client[DB_NAME]
inventario_collection = db["inventarios"]

# Verificación de conexión
try:
    client.admin.command('ping')
    print("✅ Conexión a MongoDB establecida correctamente")
except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
