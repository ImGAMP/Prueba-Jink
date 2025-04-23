import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@pytest.fixture
def api_key_header():
    return {"X-API-KEY": "XYZ123"}

# Test 1: Obtener inventario exitoso
@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_obtener_inventario(mock_find_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = {"id": 101, "nombre": "Test", "precio": 10.0}
    mock_find_one.return_value = {
        "producto_id": 101,
        "cantidad": 5,
        "historial": []
    }

    response = client.get("/inventario/101", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["producto_id"] == 101
    assert response.json()["cantidad"] == 5

# Test 2: Inventario no encontrado porque producto no existe
@patch("services.productos_client.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_inventario_no_encontrado(mock_find_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = None  # Producto no existe
    mock_find_one.return_value = None

    response = client.get("/inventario/999", headers=api_key_header)
    assert response.status_code == 404
    assert "Producto no encontrado" in response.text

# Test 3: Actualización de inventario correcta
@patch("services.productos_client.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.update_one")
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_actualizar_inventario(mock_find_one, mock_update_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = {"id": 101, "nombre": "Test"}

    # Simula el inventario antes y después de actualizar
    mock_find_one.side_effect = [
        {"producto_id": 101, "cantidad": 10, "historial": []},  # antes del update
        {"producto_id": 101, "cantidad": 8, "historial": []},   # después del update
    ]

    response = client.put("/inventario/101?cantidad_comprada=2", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["producto_id"] == 101
    assert response.json()["cantidad"] == 8

