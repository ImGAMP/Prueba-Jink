# Microservicio de Inventario - FastAPI + MongoDB

Este microservicio forma parte de una arquitectura distribuida orientada a la gestión de productos e inventario. Se encarga de almacenar y modificar la cantidad disponible de productos, así como de registrar los movimientos relacionados (como compras).

## Tecnologías utilizadas

- Python 3.12
- FastAPI
- MongoDB
- Pydantic V2
- Pytest + Coverage
- Comunicación entre microservicios vía HTTP JSON
- Seguridad basada en API Key

## Estructura del proyecto

```
inventario-service/
├── main.py                      # Entrada principal
├── models/                      # Modelos Pydantic
├── routes/                      # Rutas y lógica de API
├── services/                    # Comunicación con microservicios externos
├── utils/                       # Logger y utilidades
├── middleware/                  # Validación de API Key
├── tests/                       # Pruebas unitarias e integración
├── requirements.txt             # Dependencias
└── .env                         # Variables de entorno (API_KEY, URL productos, etc.)
```

## Instalación y ejecución local

```bash
# Clonar repositorio
git clone https://github.com/tu_usuario/inventario-service.git
cd inventario-service

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # en Linux/macOS
venv\Scripts\activate     # en Windows

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env
```

### Ejecutar el servidor

```bash
uvicorn main:app --reload
```

Accede a la documentación interactiva en:

http://localhost:8000/docs

## Seguridad

Este microservicio utiliza autenticación vía API Key.
Asegúrate de incluir el header:

```
X-API-KEY: tu_clave
```

## Ejecución de pruebas

```bash
# Ejecutar pruebas + cobertura
pytest --cov=. --cov-report=term-missing
```

## Endpoints principales

| Método | Ruta               | Descripción                             |
|--------|--------------------|-----------------------------------------|
| GET    | /inventario/{id}   | Obtener inventario de un producto       |
| PUT    | /inventario/{id}   | Actualizar cantidad tras una compra     |
| POST   | /inventario/       | Crear inventario (si no existe)         |

### Ejemplo POST:

```json
{
  "producto_id": 101,
  "cantidad": 10,
  "historial": [
    {
      "accion": "creación",
      "cantidad_cambiada": 10,
      "timestamp": "2025-04-21T10:00:00Z"
    }
  ]
}
```

## Consideraciones

- Valida si el producto existe consultando el microservicio de productos.
- Los cambios en inventario se registran en consola como eventos.
- El esquema OpenAPI está protegido por autenticación.

## Autor

Desarrollado por Gustavo Adolfo Mojica Perdigon  
Correo: gmojica@unal.edu.co  
2025 

