import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock
import httpx
from services.productos_client import obtener_producto

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

# Test 4: Fallo de conexión simulada en productos_client
@pytest.mark.asyncio
async def test_error_conexion_producto(monkeypatch):
    async def mock_error(*args, **kwargs):
        raise httpx.RequestError("Falló conexión")

    monkeypatch.setattr("httpx.AsyncClient.get", mock_error)

    result = await obtener_producto(999)
    assert result is None

# Test 5: Acceso sin API Key (middleware)
def test_acceso_sin_api_key():
    response = client.get("/inventario/101")
    assert response.status_code == 401
    assert response.json()["error"] == "API Key inválida"

# Test 6: Cobertura de custom_openapi de main.py (OpenAPI)
def test_openapi_schema(api_key_header):
    response = client.get("/openapi.json", headers=api_key_header)
    assert response.status_code == 200
    assert "paths" in response.json()
    assert "securitySchemes" in response.json()["components"]

# Test 7: Inventario con cantidad negativa
@patch("services.productos_client.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_actualizar_inventario_negativo(mock_find_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = {"id": 103, "nombre": "Negativo"}
    mock_find_one.return_value = {"producto_id": 103, "cantidad": 10, "historial": []}

    response = client.put("/inventario/103?cantidad_comprada=-2", headers=api_key_header)
    assert response.status_code == 400
    assert "cantidad debe ser positiva" in response.text

# Test 8: Inventario sin stock suficiente
@patch("services.productos_client.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_actualizar_inventario_sin_stock(mock_find_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = {"id": 104, "nombre": "Sin stock"}
    mock_find_one.return_value = {"producto_id": 104, "cantidad": 1, "historial": []}

    response = client.put("/inventario/104?cantidad_comprada=5", headers=api_key_header)
    assert response.status_code == 400
    assert "suficiente inventario" in response.text

# Test 9: Simular error HTTP diferente a 200 en productos_client
@patch("httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_producto_responde_error(mock_get):
    class MockResponse:
        status_code = 500
        def json(self):
            return {}

    mock_get.return_value = MockResponse()
    resultado = await obtener_producto(999)
    assert resultado is None

# Test 10: Llamar dos veces /openapi.json para cubrir caché de schema
def test_openapi_schema_cache(api_key_header):
    for _ in range(2):
        response = client.get("/openapi.json", headers=api_key_header)
        assert response.status_code == 200
        assert "components" in response.json()