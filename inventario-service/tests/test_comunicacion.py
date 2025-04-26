import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone
import httpx

@pytest.mark.asyncio
async def test_actualizar_inventario(async_client, api_key_header):
    """Debe actualizar el inventario correctamente."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock) as mock_producto, \
         patch("routes.inventario_routes.inventario_collection.find_one") as mock_find, \
         patch("routes.inventario_routes.inventario_collection.update_one") as mock_update:

        mock_find.side_effect = [
            {"producto_id": 101, "cantidad": 5, "historial": []},  # Estado inicial
            {"producto_id": 101, "cantidad": 3, "historial": []}   # Estado luego de la compra
        ]
        mock_producto.return_value = {"id": 101, "nombre": "Producto Test", "precio": 100.0}

        response = await async_client.put("/inventario/101?cantidad_comprada=2", headers=api_key_header)
        assert response.status_code == 200
        assert response.json()["cantidad"] == 3

@pytest.mark.asyncio
async def test_obtener_inventario_no_encontrado(async_client, api_key_header):
    """Debe retornar 404 si el inventario no existe."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock) as mock_producto, \
         patch("routes.inventario_routes.inventario_collection.find_one", return_value=None) as mock_find:

        mock_producto.return_value = {"id": 101, "nombre": "Test", "precio": 100.0}
        response = await async_client.get("/inventario/101", headers=api_key_header)
        assert response.status_code == 404
        assert "Inventario no encontrado" in response.text

@pytest.mark.asyncio
async def test_timeout_al_traer_producto(async_client, api_key_header):
    """Debe manejar timeout al consultar un producto."""
    with patch("routes.inventario_routes.obtener_producto", side_effect=httpx.RequestError("Timeout")):
        response = await async_client.get("/inventario/999", headers=api_key_header)
        assert response.status_code == 404
        assert "Producto no encontrado" in response.text

@pytest.mark.asyncio
async def test_timeout_en_creacion_inventario(async_client, api_key_header):
    """Debe manejar timeout en creación de inventario."""
    with patch("services.productos_client.httpx.AsyncClient.get", side_effect=httpx.RequestError("Timeout")):
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

@pytest.mark.asyncio
async def test_timeout_en_actualizacion(async_client, api_key_header):
    """Debe manejar timeout al actualizar inventario."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock, return_value=None), \
         patch("routes.inventario_routes.inventario_collection.find_one", return_value={"producto_id": 888, "cantidad": 20, "historial": []}):

        response = await async_client.put("/inventario/888?cantidad_comprada=1", headers=api_key_header)
        assert response.status_code == 404
        assert "Producto no encontrado" in response.text
