import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# Cargar variables de entorno
load_dotenv()

# Configuración base
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/inventario_db")
DB_NAME = os.getenv("DB_NAME", "inventario_db")

# Detectar si estamos en testing o en CI
is_testing = "pytest" in sys.modules
is_ci = os.getenv("CI") == "true"

# Opciones comunes de conexión
mongo_options = {
    'connectTimeoutMS': 5000,
    'socketTimeoutMS': 30000,
    'serverSelectionTimeoutMS': 5000
}

# Habilitar SSL solo si es ambiente productivo
if not (is_testing or is_ci):
    mongo_options.update({
        'ssl': True,
        'tlsAllowInvalidCertificates': True
    })

# Conectar a MongoDB
try:
    client = MongoClient(MONGO_URI, **mongo_options)
    db = client[DB_NAME]
    inventario_collection = db["inventarios"]

    # Probar la conexión
    client.admin.command('ping')
    print("✅ Conexión a MongoDB establecida correctamente")
except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
    raise
