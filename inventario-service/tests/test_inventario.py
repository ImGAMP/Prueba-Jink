import httpx
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone

from main import app  # Asegúrate que este importa tu FastAPI app

# ---------------- FIXTURES ----------------

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def api_key_header():
    return {"X-API-KEY": "XYZ123"}

# --------- GET /inventario/{id} ---------

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
@pytest.mark.asyncio
async def test_obtener_inventario(mock_find_one, mock_obtener_producto, async_client, api_key_header):
    mock_obtener_producto.return_value = {"id": 101, "nombre": "Test", "precio": 10.0}
    mock_find_one.return_value = {"producto_id": 101, "cantidad": 5, "historial": []}

    response = await async_client.get("/inventario/101", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["producto_id"] == 101

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
@pytest.mark.asyncio
async def test_inventario_producto_no_existe(mock_find_one, mock_obtener_producto, async_client, api_key_header):
    mock_obtener_producto.return_value = None
    mock_find_one.return_value = None

    response = await async_client.get("/inventario/999", headers=api_key_header)
    assert response.status_code == 404

# --------- PUT /inventario/{id} ---------

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.update_one")
@patch("routes.inventario_routes.inventario_collection.find_one")
@pytest.mark.asyncio
async def test_actualizar_inventario(mock_find_one, mock_update_one, mock_obtener_producto, async_client, api_key_header):
    mock_obtener_producto.return_value = {"id": 101, "nombre": "Test"}
    mock_find_one.side_effect = [
        {"producto_id": 101, "cantidad": 10, "historial": []},
        {"producto_id": 101, "cantidad": 8, "historial": []},
    ]

    response = await async_client.put("/inventario/101?cantidad_comprada=2", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["cantidad"] == 8

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
@pytest.mark.asyncio
async def test_actualizar_inventario_negativo(mock_find_one, mock_obtener_producto, async_client, api_key_header):
    mock_obtener_producto.return_value = {"id": 103, "nombre": "Negativo"}
    mock_find_one.return_value = {"producto_id": 103, "cantidad": 10, "historial": []}

    response = await async_client.put("/inventario/103?cantidad_comprada=-2", headers=api_key_header)
    assert response.status_code == 400

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
@pytest.mark.asyncio
async def test_actualizar_inventario_sin_stock(mock_find_one, mock_obtener_producto, async_client, api_key_header):
    mock_obtener_producto.return_value = {"id": 104, "nombre": "Sin stock"}
    mock_find_one.return_value = {"producto_id": 104, "cantidad": 1, "historial": []}

    response = await async_client.put("/inventario/104?cantidad_comprada=5", headers=api_key_header)
    assert response.status_code == 400

# --------- POST /inventario ---------

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
            {"accion": "creación", "cantidad_cambiada": 5, "timestamp": datetime.now(timezone.utc).isoformat()}
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

    data = {"producto_id": 102, "cantidad": 10, "historial": []}
    response = await async_client.post("/inventario/", json=data, headers=api_key_header)
    assert response.status_code == 409

# --------- Seguridad ---------

@pytest.mark.asyncio
async def test_acceso_sin_api_key(async_client):
    response = await async_client.get("/inventario/101")
    assert response.status_code == 401
    assert response.json()["error"] == "API Key inválida"

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock, side_effect=httpx.RequestError("Timeout"))
@pytest.mark.asyncio
async def test_obtener_inventario_timeout(mock_obtener, async_client, api_key_header):
    response = await async_client.get("/inventario/999", headers=api_key_header)
    assert response.status_code == 404
    assert "error de conexión" in response.text

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_consultar_producto_valido(mock_obtener, async_client, api_key_header):
    mock_obtener.return_value = {"id": 101, "nombre": "Mocked", "precio": 88.8}
    response = await async_client.get("/inventario/consultar-producto/101", headers=api_key_header)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["data"]["type"] == "productos"
    assert json_data["data"]["attributes"]["nombre"] == "Mocked"

@patch("routes.inventario_routes.obtener_producto", return_value=None)
@pytest.mark.asyncio
async def test_consultar_producto_no_encontrado(mock_obtener, async_client, api_key_header):
    response = await async_client.get("/inventario/consultar-producto/999", headers=api_key_header)
    assert response.status_code == 404
    assert "Producto no encontrado" in response.text

@pytest.mark.asyncio
async def test_healthcheck(async_client, api_key_header):
    response = await async_client.get("/inventario/health", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("services.productos_client.httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_cliente_producto_sin_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = lambda: {}

    from services.productos_client import obtener_producto
    result = await obtener_producto(111)
    assert result is None

@patch("services.productos_client.httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_cliente_producto_sin_attributes(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = lambda: {"data": {"id": 111, "nombre": "Solo"}}

    from services.productos_client import obtener_producto
    result = await obtener_producto(111)
    assert result["nombre"] == "Solo"

@patch("services.productos_client.httpx.AsyncClient.get", side_effect=httpx.HTTPStatusError("Boom", request=None, response=None))
@pytest.mark.asyncio
async def test_cliente_producto_http_status_error(mock_get):
    from services.productos_client import obtener_producto
    result = await obtener_producto(999)
    assert result is None