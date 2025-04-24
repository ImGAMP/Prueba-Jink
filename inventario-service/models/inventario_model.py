from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from pydantic.config import ConfigDict

class MovimientoInventario(BaseModel):
    accion: str
    cantidad_cambiada: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Inventario(BaseModel):
    producto_id: int = Field(...)
    cantidad: int = Field(..., ge=0)
    historial: Optional[List[MovimientoInventario]] = []

    model_config = ConfigDict(
        json_schema_extra={
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
    )
