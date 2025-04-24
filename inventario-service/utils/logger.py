import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("inventario")

def registrar_evento(accion: str, producto_id: int, cantidad: int):
    logger.info(f"Acción: {accion.upper()} | Producto ID: {producto_id} | Cantidad modificada: {cantidad}")
