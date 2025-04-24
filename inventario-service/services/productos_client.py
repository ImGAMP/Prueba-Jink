import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PRODUCTOS_URL = os.getenv("PRODUCTOS_SERVICE_URL")
API_KEY = os.getenv("API_KEY")

async def obtener_producto(producto_id: int):
    url = f"{PRODUCTOS_URL}/productos/{producto_id}"
    headers = {"X-API-KEY": API_KEY}
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            return None
    except httpx.RequestError as e:
        # Log con mayor detalle
        print(f"[ERROR] No se pudo obtener el producto {producto_id}: {str(e)}")
        return None
    except httpx.HTTPStatusError as e:  
        # Log con mayor detalle
        print(f"[ERROR] Error al obtener el producto {producto_id}: {str(e)}")
        return None