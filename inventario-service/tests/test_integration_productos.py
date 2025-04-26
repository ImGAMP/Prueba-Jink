import os
import pytest
import time
from httpx import AsyncClient
from tenacity import retry, stop_after_attempt, wait_fixed

# Configuración de URLs y Headers
PRODUCTOS_URL = os.getenv("PRODUCTOS_SERVICE_URL", "http://producto-app:8080")
INVENTARIO_URL = os.getenv("INVENTARIO_SERVICE_URL", "http://inventario-service:8000")
HEADERS = {"X-API-KEY": os.getenv("API_KEY", "XYZ123")}

# Retry automático: 5 intentos, espera 3 segundos entre intentos
@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
async def safe_post(client, url, json=None, headers=None):
    response = await client.post(url, json=json, headers=headers, timeout=10.0)
    response.raise_for_status()
    return response

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
async def safe_get(client, url, headers=None):
    response = await client.get(url, headers=headers, timeout=10.0)
    response.raise_for_status()
    return response

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
async def safe_put(client, url, json=None, headers=None):
    response = await client.put(url, json=json, headers=headers, timeout=10.0)
    response.raise_for_status()
    return response

@pytest.mark.integration
@pytest.mark.asyncio
async def test_flujo_completo_inventario_y_productos():
    """Test de integración PRO entre inventario-service y producto-app."""

    async with AsyncClient() as client:
        # 1. Crear producto
        producto_payload = {"nombre": "Producto Test Full", "precio": 500.00}
        res_producto = await safe_post(client, f"{PRODUCTOS_URL}/productos", json=producto_payload, headers=HEADERS)
        producto_data = res_producto.json()["data"]
        producto_id = int(producto_data["id"])

        assert producto_data["attributes"]["nombre"] == "Producto Test Full"
        assert float(producto_data["attributes"]["precio"]) == 500.00

        # 2. Consultar producto desde inventario
        res_consulta = await safe_get(client, f"{INVENTARIO_URL}/inventario/consultar-producto/{producto_id}", headers=HEADERS)
        consulta_data = res_consulta.json()["data"]["attributes"]

        assert consulta_data["nombre"] == "Producto Test Full"

        # 3. Crear inventario
        inventario_payload = {
            "producto_id": producto_id,
            "cantidad": 10,
            "historial": []
        }
        res_inventario = await safe_post(client, f"{INVENTARIO_URL}/inventario/", json=inventario_payload, headers=HEADERS)
        inventario_response = res_inventario.json()

        assert inventario_response["producto_id"] == producto_id
        assert inventario_response["cantidad"] == 10

        # 4. Simular compra
        res_compra = await safe_put(client, f"{INVENTARIO_URL}/inventario/{producto_id}?cantidad_comprada=3", headers=HEADERS)
        compra_response = res_compra.json()

        assert compra_response["cantidad"] == 7

        # 5. Verificar estado final
        res_final = await safe_get(client, f"{INVENTARIO_URL}/inventario/{producto_id}", headers=HEADERS)
        final_data = res_final.json()

        assert final_data["cantidad"] == 7
        assert isinstance(final_data["historial"], list)
        assert len(final_data["historial"]) >= 1

