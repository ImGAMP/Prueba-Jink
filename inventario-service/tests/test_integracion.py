import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_crear_inventario(async_client, api_key_header):
    """Debe crear un inventario nuevo correctamente."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock) as mock_producto, \
         patch("routes.inventario_routes.inventario_collection.insert_one") as mock_insert, \
         patch("routes.inventario_routes.inventario_collection.find_one", return_value=None):

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

@pytest.mark.asyncio
async def test_crear_inventario_duplicado(async_client, api_key_header):
    """Debe impedir crear un inventario duplicado."""
    with patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock) as mock_producto, \
         patch("routes.inventario_routes.inventario_collection.find_one") as mock_find:

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
