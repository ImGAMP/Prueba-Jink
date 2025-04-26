import httpx
import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone

# ---------------- TESTS ----------------

@pytest.mark.asyncio
async def test_obtener_inventario(async_client, api_key_header):
    """Debe obtener el inventario de un producto existente."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock) as mock_producto, \
         patch("routes.inventario_routes.inventario_collection.find_one") as mock_find:

        mock_producto.return_value = {"id": 101, "nombre": "Test", "precio": 10.0}
        mock_find.return_value = {"producto_id": 101, "cantidad": 5, "historial": []}

        response = await async_client.get("/inventario/101", headers=api_key_header)
        assert response.status_code == 200
        assert response.json()["producto_id"] == 101

@pytest.mark.asyncio
async def test_inventario_producto_no_existe(async_client, api_key_header):
    """Debe devolver 404 si el producto no existe."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock) as mock_producto, \
         patch("routes.inventario_routes.inventario_collection.find_one") as mock_find:

        mock_producto.return_value = None
        mock_find.return_value = None

        response = await async_client.get("/inventario/999", headers=api_key_header)
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_actualizar_inventario(async_client, api_key_header):
    """Debe actualizar correctamente el inventario."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock) as mock_producto, \
         patch("routes.inventario_routes.inventario_collection.update_one"), \
         patch("routes.inventario_routes.inventario_collection.find_one") as mock_find:

        mock_producto.return_value = {"id": 101, "nombre": "Test"}
        mock_find.side_effect = [
            {"producto_id": 101, "cantidad": 10, "historial": []},
            {"producto_id": 101, "cantidad": 8, "historial": []},
        ]

        response = await async_client.put("/inventario/101?cantidad_comprada=2", headers=api_key_header)
        assert response.status_code == 200
        assert response.json()["cantidad"] == 8

@pytest.mark.asyncio
async def test_actualizar_inventario_negativo(async_client, api_key_header):
    """Debe fallar al actualizar con cantidad negativa."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock), \
         patch("routes.inventario_routes.inventario_collection.find_one", return_value={"producto_id": 103, "cantidad": 10, "historial": []}):

        response = await async_client.put("/inventario/103?cantidad_comprada=-2", headers=api_key_header)
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_actualizar_inventario_sin_stock(async_client, api_key_header):
    """Debe fallar si la cantidad comprada supera el stock."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock), \
         patch("routes.inventario_routes.inventario_collection.find_one", return_value={"producto_id": 104, "cantidad": 1, "historial": []}):

        response = await async_client.put("/inventario/104?cantidad_comprada=5", headers=api_key_header)
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_crear_inventario(async_client, api_key_header):
    """Debe crear un inventario correctamente."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock) as mock_producto, \
         patch("routes.inventario_routes.inventario_collection.insert_one"), \
         patch("routes.inventario_routes.inventario_collection.find_one", return_value=None):

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

@pytest.mark.asyncio
async def test_crear_inventario_duplicado(async_client, api_key_header):
    """Debe evitar crear inventario duplicado."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock), \
         patch("routes.inventario_routes.inventario_collection.find_one", return_value={"producto_id": 102, "cantidad": 10, "historial": []}):

        data = {"producto_id": 102, "cantidad": 10, "historial": []}
        response = await async_client.post("/inventario/", json=data, headers=api_key_header)
        assert response.status_code == 409

@pytest.mark.asyncio
async def test_acceso_sin_api_key(async_client):
    """Debe rechazar acceso sin API Key."""
    response = await async_client.get("/inventario/101")
    assert response.status_code == 401
    assert response.json()["error"] == "API Key inválida"

@pytest.mark.asyncio
async def test_obtener_inventario_timeout(async_client, api_key_header):
    """Debe manejar timeout al consultar inventario."""
    with patch("routes.inventario_routes.obtener_producto", side_effect=httpx.RequestError("Timeout")):
        response = await async_client.get("/inventario/999", headers=api_key_header)
        assert response.status_code == 404
        assert "error de conexión" in response.text

@pytest.mark.asyncio
async def test_consultar_producto_valido(async_client, api_key_header):
    """Debe consultar un producto exitosamente."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock) as mock_obtener:
        mock_obtener.return_value = {"id": 101, "nombre": "Mocked", "precio": 88.8}
        response = await async_client.get("/inventario/consultar-producto/101", headers=api_key_header)
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["data"]["attributes"]["nombre"] == "Mocked"

@pytest.mark.asyncio
async def test_consultar_producto_no_encontrado(async_client, api_key_header):
    """Debe retornar 404 si no encuentra producto."""
    with patch("routes.inventario_routes.obtener_producto", return_value=None):
        response = await async_client.get("/inventario/consultar-producto/999", headers=api_key_header)
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_healthcheck(async_client, api_key_header):
    """Debe retornar estado de salud ok."""
    response = await async_client.get("/inventario/health", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# --- PRUEBAS DE CLIENTE PRODUCTO ---

@pytest.mark.asyncio
async def test_cliente_producto_sin_data():
    """Debe retornar None si no hay data."""
    with patch("services.productos_client.httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: {}

        from services.productos_client import obtener_producto
        result = await obtener_producto(111)
        assert result is None

@pytest.mark.asyncio
async def test_cliente_producto_sin_attributes():
    """Debe manejar producto sin attributes."""
    with patch("services.productos_client.httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: {"data": {"id": 111, "nombre": "Solo"}}

        from services.productos_client import obtener_producto
        result = await obtener_producto(111)
        assert result["nombre"] == "Solo"

@pytest.mark.asyncio
async def test_cliente_producto_http_status_error():
    """Debe retornar None si hay error HTTP."""
    with patch("services.productos_client.httpx.AsyncClient.get", side_effect=httpx.HTTPStatusError("Boom", request=None, response=None)):
        from services.productos_client import obtener_producto
        result = await obtener_producto(999)
        assert result is None
