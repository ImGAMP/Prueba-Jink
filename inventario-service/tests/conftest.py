import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
async def clean_db():
    # Limpiar la base de datos antes de cada test
    from config import inventario_collection
    await inventario_collection.delete_many({})
