from fastapi import FastAPI
from routes.inventario_routes import router as inventario_router
from middleware.api_key_validator import api_key_middleware
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="Microservicio de Inventario")

# Middleware de API Key
app.middleware("http")(api_key_middleware)

# Rutas
app.include_router(inventario_router, prefix="/inventario", tags=["Inventario"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "services": {"mongo": "up", "productos": "up"}}

@app.get("/ping")
def ping():
    return {"msg": "pong actualizado"}

# Swagger personalizado

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Microservicio de Inventario",
        version="1.0.0",
        description="Endpoints protegidos con API Key",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY"
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"ApiKeyAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
