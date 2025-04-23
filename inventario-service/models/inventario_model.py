from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MovimientoInventario(BaseModel):
    accion: str
    cantidad_cambiada: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Inventario(BaseModel):
    producto_id: int = Field(..., example=101)
    cantidad: int = Field(..., ge=0, example=10)
    historial: Optional[List[MovimientoInventario]] = []

    class Config:
        schema_extra = {
            "example": {
                "producto_id": 101,
                "cantidad": 15,
                "historial": [
                    {
                        "accion": "compra",
                        "cantidad_cambiada": -1,
                        "timestamp": "2025-04-22T10:00:00Z"
                    }
                ]
            }
        }