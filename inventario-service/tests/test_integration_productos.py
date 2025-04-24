import pytest
from httpx import AsyncClient
from main import app  
import os

@pytest.mark.asyncio
async def test_obtener_producto_desde_microservicio():
    producto_id = 1  # Asegúrate de que este producto exista en el microservicio de productos

    async with AsyncClient(app=app, base_url="http://test") as client:
        headers = {"X-API-KEY": os.getenv("API_KEY", "XYZ123")}
        response = await client.get(f"/inventario/consultar-producto/{producto_id}", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["id"] == producto_id
        assert "nombre" in data["data"]
        assert "precio" in data["data"]
