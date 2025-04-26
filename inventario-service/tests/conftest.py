import pytest
import os
from httpx import AsyncClient
from main import app

@pytest.fixture
async def async_client():
    """Cliente HTTP asíncrono para pruebas."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def producto_service_url():
    """URL base del servicio de productos."""
    return os.getenv("PRODUCTOS_SERVICE_URL", "http://producto-app:8080")

@pytest.fixture
def api_key_header():
    """Cabecera de autorización simulando API KEY."""
    return {"X-API-KEY": os.getenv("API_KEY", "XYZ123")}

@pytest.fixture(autouse=True)
async def clean_db():
    """Limpia la colección de inventario antes de cada test."""
    from config import inventario_collection
    await inventario_collection.delete_many({})
