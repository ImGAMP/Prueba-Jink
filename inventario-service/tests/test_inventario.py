import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock
import httpx
from datetime import datetime, timezone

client = TestClient(app)

@pytest.fixture
def api_key_header():
    return {"X-API-KEY": "XYZ123"}

# --------- GET /inventario/{id} ---------

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_obtener_inventario(mock_find_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = {"id": 101, "nombre": "Test", "precio": 10.0}
    mock_find_one.return_value = {"producto_id": 101, "cantidad": 5, "historial": []}

    response = client.get("/inventario/101", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["producto_id"] == 101
    assert response.json()["cantidad"] == 5

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_inventario_producto_no_existe(mock_find_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = None
    mock_find_one.return_value = None

    response = client.get("/inventario/999", headers=api_key_header)
    assert response.status_code == 404
    assert "Producto no encontrado" in response.text

# --------- PUT /inventario/{id} ---------

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.update_one")
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_actualizar_inventario(mock_find_one, mock_update_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = {"id": 101, "nombre": "Test"}
    mock_find_one.side_effect = [
        {"producto_id": 101, "cantidad": 10, "historial": []},
        {"producto_id": 101, "cantidad": 8, "historial": []},
    ]

    response = client.put("/inventario/101?cantidad_comprada=2", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["cantidad"] == 8

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_actualizar_inventario_negativo(mock_find_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = {"id": 103, "nombre": "Negativo"}
    mock_find_one.return_value = {"producto_id": 103, "cantidad": 10, "historial": []}

    response = client.put("/inventario/103?cantidad_comprada=-2", headers=api_key_header)
    assert response.status_code == 400
    assert "cantidad debe ser positiva" in response.text

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_actualizar_inventario_sin_stock(mock_find_one, mock_obtener_producto, api_key_header):
    mock_obtener_producto.return_value = {"id": 104, "nombre": "Sin stock"}
    mock_find_one.return_value = {"producto_id": 104, "cantidad": 1, "historial": []}

    response = client.put("/inventario/104?cantidad_comprada=5", headers=api_key_header)
    assert response.status_code == 400
    assert "suficiente inventario" in response.text

# --------- POST /inventario ---------

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.insert_one")
@patch("routes.inventario_routes.inventario_collection.find_one", return_value=None)
def test_crear_inventario(mock_find, mock_insert, mock_producto, api_key_header):
    mock_producto.return_value = {"id": 101, "nombre": "Test", "precio": 100.0}
    data = {
        "producto_id": 101,
        "cantidad": 5,
        "historial": [
            {"accion": "creación", "cantidad_cambiada": 5, "timestamp": datetime.now(timezone.utc).isoformat()}
        ]
    }
    response = client.post("/inventario/", json=data, headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["producto_id"] == 101

@patch("routes.inventario_routes.obtener_producto", new_callable=AsyncMock)
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_crear_inventario_duplicado(mock_find, mock_producto, api_key_header):
    mock_producto.return_value = {"id": 102, "nombre": "Test", "precio": 100.0}
    mock_find.return_value = {"producto_id": 102, "cantidad": 10, "historial": []}

    data = {"producto_id": 102, "cantidad": 10, "historial": []}
    response = client.post("/inventario/", json=data, headers=api_key_header)
    assert response.status_code == 409
    assert "ya existe" in response.text

# --------- Errores y seguridad ---------

def test_acceso_sin_api_key():
    response = client.get("/inventario/101")
    assert response.status_code == 401
    assert response.json()["error"] == "API Key inválida"

@patch("httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_producto_responde_error(mock_get):
    class MockResponse:
        status_code = 500
        def json(self): return {}
    mock_get.return_value = MockResponse()
    from services.productos_client import obtener_producto
    resultado = await obtener_producto(999)
    assert resultado is None

@pytest.mark.asyncio
async def test_error_conexion_producto(monkeypatch):
    async def mock_error(*args, **kwargs):
        raise httpx.RequestError("Falló conexión")
    monkeypatch.setattr("httpx.AsyncClient.get", mock_error)
    from services.productos_client import obtener_producto
    resultado = await obtener_producto(999)
    assert resultado is None
