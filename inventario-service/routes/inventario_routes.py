from fastapi import APIRouter, HTTPException
from models.inventario_model import Inventario, MovimientoInventario
from config import inventario_collection
from services.productos_client import obtener_producto
from utils.logger import registrar_evento
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime, timezone
from fastapi import APIRouter, Path
from services.productos_client import obtener_producto
from fastapi.responses import JSONResponse
from httpx import RequestError

router = APIRouter()


@router.get("/consultar-producto/{producto_id}")
async def consultar_producto(producto_id: int = Path(..., gt=0)):
    try:
        producto = await obtener_producto(producto_id)
    except RequestError:
        raise HTTPException(status_code=404, detail="Producto no encontrado (error de conexión)")

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    jsonapi_response = {
        "data": {
            "type": "productos",
            "id": str(producto.get("id")),
            "attributes": {
                "nombre": producto.get("nombre"),
                "precio": producto.get("precio")
            }
        }
    }
    return JSONResponse(content=jsonapi_response)


@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/{producto_id}", response_model=Inventario)
async def obtener_inventario(producto_id: int):
    try:
        producto = await obtener_producto(producto_id)
    except RequestError:  # <- ¡Este import es clave!
        raise HTTPException(status_code=404, detail="Producto no encontrado (error de conexión)")

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    inventario = inventario_collection.find_one({"producto_id": producto_id})
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado para este producto")

    return Inventario(**inventario)

@router.put("/{producto_id}", response_model=Inventario)
async def actualizar_inventario(producto_id: int, cantidad_comprada: int):
    if cantidad_comprada <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser positiva")

    producto = await obtener_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    inventario = inventario_collection.find_one({"producto_id": producto_id})
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")

    nueva_cantidad = inventario["cantidad"] - cantidad_comprada
    if nueva_cantidad < 0:
        raise HTTPException(status_code=400, detail="No hay suficiente inventario disponible")

    movimiento = {
        "accion": "compra",
        "cantidad_cambiada": -cantidad_comprada,
        "timestamp": datetime.now(timezone.utc)
    }
    inventario_collection.update_one(
        {"producto_id": producto_id},
        {"$set": {"cantidad": nueva_cantidad}, "$push": {"historial": movimiento}}
    )

    registrar_evento("compra", producto_id, -cantidad_comprada)

    inventario_actualizado = inventario_collection.find_one({"producto_id": producto_id})
    return Inventario(**inventario_actualizado)

@router.post("/", response_model=Inventario)
async def crear_inventario(inventario: Inventario):
    producto = await obtener_producto(inventario.producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    existente = inventario_collection.find_one({"producto_id": inventario.producto_id})
    if existente:
        raise HTTPException(status_code=409, detail="El inventario de este producto ya existe")

    inventario_dict = inventario.model_dump()
    inventario_collection.insert_one(inventario_dict)
    registrar_evento("creación", inventario.producto_id, inventario.cantidad)
    return inventario
