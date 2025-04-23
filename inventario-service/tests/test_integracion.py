import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def api_key_header():
    return {"X-API-KEY": "XYZ123"}

@patch("routes.inventario_routes.obtener_producto")
@patch("routes.inventario_routes.inventario_collection.insert_one")
@patch("routes.inventario_routes.inventario_collection.find_one", return_value=None)
def test_crear_inventario(mock_find, mock_insert, mock_producto, api_key_header):
    mock_producto.return_value = {"id": 101, "nombre": "Test", "precio": 100.0}
    data = {
        "producto_id": 101,
        "cantidad": 5,
        "historial": [
            {
                "accion": "creación",
                "cantidad_cambiada": 5,
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    }
    response = client.post("/inventario/", json=data, headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["producto_id"] == 101

@patch("routes.inventario_routes.obtener_producto")
@patch("routes.inventario_routes.inventario_collection.find_one")
def test_crear_inventario_duplicado(mock_find, mock_producto, api_key_header):
    mock_producto.return_value = {"id": 102, "nombre": "Test", "precio": 100.0}
    mock_find.return_value = {"producto_id": 102, "cantidad": 10, "historial": []}
    data = {
        "producto_id": 102,
        "cantidad": 10,
        "historial": []
    }
    response = client.post("/inventario/", json=data, headers=api_key_header)
    assert response.status_code == 409
    assert "ya existe" in response.text
