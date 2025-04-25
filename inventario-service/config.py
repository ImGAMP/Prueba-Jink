import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Configuración base
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "inventario_db")

# Detección automática de entorno
is_testing = "pytest" in sys.modules
is_ci = os.getenv("CI") == "true"  # Variable automática en GitHub Actions

# Configuración común
mongo_options = {
    'connectTimeoutMS': 5000,
    'socketTimeoutMS': 30000,
    'serverSelectionTimeoutMS': 5000
}

# SSL solo en producción (no en testing ni CI)
if not (is_testing or is_ci):
    mongo_options.update({
        'ssl': True,
        'tlsAllowInvalidCertificates': True  # Opción moderna compatible
    })

# Conexión a MongoDB
try:
    client = MongoClient(MONGO_URI, **mongo_options)
    db = client[DB_NAME]
    inventario_collection = db["inventarios"]
    
    # Verificación rápida de conexión
    client.admin.command('ping')
    print("✅ Conexión a MongoDB establecida correctamente")
except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
    raise  # Falla rápido en caso de error
