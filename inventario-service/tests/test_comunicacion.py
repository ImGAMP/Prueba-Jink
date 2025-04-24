import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime, timezone
from main import app
import httpx

client = TestClient(app)

@pytest.fixture
def api_key_header():
    return {"X-API-KEY": "XYZ123"}

@patch("routes.inventario_routes.obtener_producto")
@patch("routes.inventario_routes.inventario_collection.find_one")
@patch("routes.inventario_routes.inventario_collection.update_one")
def test_actualizar_inventario(mock_update, mock_find, mock_producto, api_key_header):
    mock_find.side_effect = [
        {"producto_id": 101, "cantidad": 5, "historial": []},  # inventario inicial
        {"producto_id": 101, "cantidad": 3, "historial": []}   # inventario actualizado
    ]
    mock_producto.return_value = {"id": 101, "nombre": "Producto Test", "precio": 100.0}

    response = client.put("/inventario/101?cantidad_comprada=2", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["cantidad"] == 3

@patch("routes.inventario_routes.obtener_producto")
@patch("routes.inventario_routes.inventario_collection.find_one", return_value=None)
def test_obtener_inventario_no_encontrado(mock_find, mock_producto, api_key_header):
    mock_producto.return_value = {"id": 101, "nombre": "Test", "precio": 100.0}
    response = client.get("/inventario/101", headers=api_key_header)
    assert response.status_code == 404
    assert "Inventario no encontrado" in response.text


@patch("services.productos_client.httpx.AsyncClient.get", side_effect=httpx.RequestError("Timeout"))
def test_timeout_al_traer_producto(mock_httpx, api_key_header):
    response = client.get("/inventario/999", headers=api_key_header)
    assert response.status_code == 404
    assert "Producto no encontrado" in response.text

@patch("services.productos_client.httpx.AsyncClient.get", side_effect=httpx.RequestError("Timeout"))
def test_timeout_en_creacion_inventario(mock_httpx, api_key_header):
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
    response = client.post("/inventario/", json=data, headers=api_key_header)
    assert response.status_code == 404
    assert "Producto no encontrado" in response.text

@patch("routes.inventario_routes.obtener_producto", return_value=None)
@patch("routes.inventario_routes.inventario_collection.find_one", return_value={"producto_id": 888, "cantidad": 20, "historial": []})
def test_timeout_en_actualizacion(mock_find, mock_producto, api_key_header):
    response = client.put("/inventario/888?cantidad_comprada=1", headers=api_key_header)
    assert response.status_code == 404
    assert "Producto no encontrado" in response.text
