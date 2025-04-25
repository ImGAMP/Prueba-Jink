import os
import pytest
from httpx import AsyncClient
import time

# Configuración dinámica para ambientes locales y CI
PRODUCTOS_URL = os.getenv("PRODUCTOS_SERVICE_URL", "http://producto-app:8080")
INVENTARIO_URL = os.getenv("INVENTARIO_SERVICE_URL", "http://inventario-service:8000")
HEADERS = {"X-API-KEY": os.getenv("API_KEY", "XYZ123")}

@pytest.mark.integration
@pytest.mark.asyncio
async def test_flujo_completo_inventario_y_productos():
    """Test de integración real entre los servicios"""
    max_retries = 5
    retry_delay = 3
    
    async with AsyncClient() as client:
        # 1. Crear producto con reintentos
        producto_payload = {"nombre": "Producto Test Full", "precio": 500.00}
        res_producto = None
        
        for attempt in range(max_retries):
            try:
                res_producto = await client.post(
                    f"{PRODUCTOS_URL}/productos",
                    json=producto_payload,
                    headers=HEADERS,
                    timeout=10.0
                )
                if res_producto.status_code == 200:
                    break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(retry_delay)
        
        assert res_producto.status_code == 200, f"Error al crear producto: {res_producto.text}"
        producto_json = res_producto.json()
        producto_id = int(producto_json["data"]["id"])

        # 2. Verificar acceso desde inventario
        res_consulta = await client.get(
            f"{INVENTARIO_URL}/inventario/consultar-producto/{producto_id}",
            headers=HEADERS,
            timeout=10.0
        )
        assert res_consulta.status_code == 200
        consulta_json = res_consulta.json()
        assert consulta_json["data"]["attributes"]["nombre"] == "Producto Test Full"

        # 3. Crear inventario
        inventario_payload = {
            "producto_id": producto_id,
            "cantidad": 10,
            "historial": []
        }
        res_inventario = await client.post(
            f"{INVENTARIO_URL}/inventario/",
            json=inventario_payload,
            headers=HEADERS,
            timeout=10.0
        )
        assert res_inventario.status_code == 200

        # 4. Simular compra
        res_compra = await client.put(
            f"{INVENTARIO_URL}/inventario/{producto_id}?cantidad_comprada=3",
            headers=HEADERS,
            timeout=10.0
        )
        assert res_compra.status_code == 200

        # 5. Verificar estado final
        res_final = await client.get(
            f"{INVENTARIO_URL}/inventario/{producto_id}",
            headers=HEADERS,
            timeout=10.0
        )
        assert res_final.status_code == 200
        final_data = res_final.json()
        assert final_data["cantidad"] == 7
        assert len(final_data["historial"]) == 1
