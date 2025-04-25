import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone
from main import app

# ---------------- FIXTURES ----------------

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def api_key_header():
    return {"X-API-KEY": "XYZ123"}

# ---------------- TESTS ----------------

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.insert_one")
@patch("routes.inventario_routes.inventario_collection.find_one", return_value=None)
@pytest.mark.asyncio
async def test_crear_inventario(mock_find, mock_insert, mock_producto, async_client, api_key_header):
    mock_producto.return_value = {"id": 101, "nombre": "Test", "precio": 100.0}
    data = {
        "producto_id": 101,
        "cantidad": 5,
        "historial": [
            {
                "accion": "creación",
                "cantidad_cambiada": 5,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        ]
    }
    response = await async_client.post("/inventario/", json=data, headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["producto_id"] == 101

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
@pytest.mark.asyncio
async def test_crear_inventario_duplicado(mock_find, mock_producto, async_client, api_key_header):
    mock_producto.return_value = {"id": 102, "nombre": "Test", "precio": 100.0}
    mock_find.return_value = {"producto_id": 102, "cantidad": 10, "historial": []}
    data = {
        "producto_id": 102,
        "cantidad": 10,
        "historial": []
    }
    response = await async_client.post("/inventario/", json=data, headers=api_key_header)
    assert response.status_code == 409
    assert "ya existe" in response.text
