import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone
from main import app
import httpx

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
@patch("routes.inventario_routes.inventario_collection.find_one")
@patch("routes.inventario_routes.inventario_collection.update_one")
@pytest.mark.asyncio
async def test_actualizar_inventario(mock_update, mock_find, mock_producto, async_client, api_key_header):
    mock_find.side_effect = [
        {"producto_id": 101, "cantidad": 5, "historial": []},  # inventario inicial
        {"producto_id": 101, "cantidad": 3, "historial": []}   # inventario actualizado
    ]
    mock_producto.return_value = {"id": 101, "nombre": "Producto Test", "precio": 100.0}

    response = await async_client.put("/inventario/101?cantidad_comprada=2", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["cantidad"] == 3

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one", return_value=None)
@pytest.mark.asyncio
async def test_obtener_inventario_no_encontrado(mock_find, mock_producto, async_client, api_key_header):
    mock_producto.return_value = {"id": 101, "nombre": "Test", "precio": 100.0}
    response = await async_client.get("/inventario/101", headers=api_key_header)
    assert response.status_code == 404
    assert "Inventario no encontrado" in response.text

@patch("routes.inventario_routes.obtener_producto", side_effect=httpx.RequestError("Timeout"))
@pytest.mark.asyncio
async def test_timeout_al_traer_producto(mock_get, async_client, api_key_header):
    response = await async_client.get("/inventario/999", headers=api_key_header)
    assert response.status_code == 404
    assert "Producto no encontrado" in response.text

@patch("services.productos_client.httpx.AsyncClient.get", side_effect=httpx.RequestError("Timeout"))
@pytest.mark.asyncio
async def test_timeout_en_creacion_inventario(mock_httpx, async_client, api_key_header):
    data = {
        "producto_id": 555,
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
    assert response.status_code == 404
    assert "Producto no encontrado" in response.text

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock, return_value=None)
@patch("routes.inventario_routes.inventario_collection.find_one", return_value={"producto_id": 888, "cantidad": 20, "historial": []})
@pytest.mark.asyncio
async def test_timeout_en_actualizacion(mock_find, mock_producto, async_client, api_key_header):
    response = await async_client.put("/inventario/888?cantidad_comprada=1", headers=api_key_header)
    assert response.status_code == 404
    assert "Producto no encontrado" in response.text
