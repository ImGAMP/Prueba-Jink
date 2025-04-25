import os
import pytest
from httpx import AsyncClient

PRODUCTOS_URL = "http://producto-app:8080"
INVENTARIO_URL = "http://localhost:8000"
HEADERS = {"X-API-KEY": os.getenv("API_KEY", "XYZ123")}

@pytest.mark.asyncio
async def test_flujo_completo_inventario_y_productos():
    # 1. Crear producto
    producto_payload = {"nombre": "Producto Test Full", "precio": 500.00}

    async with AsyncClient() as client:
        res_producto = await client.post(f"{PRODUCTOS_URL}/productos", json=producto_payload, headers=HEADERS)
        assert res_producto.status_code == 200, f"Error al crear producto: {res_producto.text}"
        producto_json = res_producto.json()
        producto_id = int(producto_json["data"]["id"])

        # 2. Verificar acceso desde inventario (consultar-producto)
        res_consulta = await client.get(f"{INVENTARIO_URL}/inventario/consultar-producto/{producto_id}", headers=HEADERS)
        assert res_consulta.status_code == 200, f"Error al consultar producto desde inventario: {res_consulta.text}"
        consulta_json = res_consulta.json()
        assert consulta_json["data"]["attributes"]["nombre"] == "Producto Test Full"

        # 3. Crear inventario para el producto
        inventario_payload = {
            "producto_id": producto_id,
            "cantidad": 10,
            "historial": []
        }
        res_inventario = await client.post(f"{INVENTARIO_URL}/inventario/", json=inventario_payload, headers=HEADERS)
        assert res_inventario.status_code == 200, f"Error al crear inventario: {res_inventario.text}"
        inventario_json = res_inventario.json()
        assert inventario_json["producto_id"] == producto_id
        assert inventario_json["cantidad"] == 10

        # 4. Simular compra (reducción de inventario)
        res_compra = await client.put(
            f"{INVENTARIO_URL}/inventario/{producto_id}?cantidad_comprada=3",
            headers=HEADERS
        )
        assert res_compra.status_code == 200, f"Error al simular compra: {res_compra.text}"
        post_compra_json = res_compra.json()
        assert post_compra_json["cantidad"] == 7

        # 5. Obtener inventario final y validar historial
        res_final = await client.get(f"{INVENTARIO_URL}/inventario/{producto_id}", headers=HEADERS)
        assert res_final.status_code == 200
        final_data = res_final.json()
        assert final_data["cantidad"] == 7
        assert len(final_data["historial"]) == 1
        assert final_data["historial"][0]["accion"] == "compra"