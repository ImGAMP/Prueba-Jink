from fastapi import APIRouter, HTTPException
from models.inventario_model import Inventario, MovimientoInventario
from config import inventario_collection
from services.productos_client import obtener_producto
from utils.logger import registrar_evento
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/{producto_id}", response_model=Inventario)
async def obtener_inventario(producto_id: int):
    producto = await obtener_producto(producto_id)
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

    # ✅ Validación del producto para cubrir fallos de comunicación o inexistencia
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
