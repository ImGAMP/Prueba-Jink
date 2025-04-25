# Guía de Implementación Técnica

## Estructura del Proyecto

La solución se compone de dos microservicios:
- `producto-app`: Microservicio en Java (Spring Boot) que gestiona productos.
- `inventario-service`: Microservicio en Python (FastAPI) que gestiona inventarios y consulta productos por HTTP.

Ambos servicios se orquestan con Docker Compose y comparten una red virtual.

## Patrones de Diseño

- **Separación de responsabilidades**: Servicios claramente separados por dominio.
- **DTOs y mappers**: Uso de DTOs en `producto-app` para encapsular la lógica de entrada/salida.
- **Client service**: Comunicación HTTP entre servicios encapsulada en un cliente dedicado (`productos_client.py`).
- **Logs estructurados**: Inclusión de correlationId en todos los logs.
- **Exception handling global**: Manejadores centralizados de errores.

## Versionado de API

Actualmente se maneja una única versión base (v1). Se recomienda:
- Incluir `/v1` en todos los endpoints de forma explícita.
- Mantener contratos estables por versión.
- Usar headers o query params para pruebas con nuevas versiones.

## Recomendaciones de Desarrollo

- Seguir el estándar JSON:API en todos los endpoints.
- Utilizar `@Validated` en controladores Spring y `Pydantic` en FastAPI para validaciones de entrada.
- Añadir pruebas unitarias para cada endpoint (mocking en integración).
- Mantener documentación Swagger actualizada.
- Utilizar variables de entorno desde `.env` o `docker-compose.yml`.

## Escalabilidad y Mejoras Futuras

- **Mensajería asíncrona**: Reemplazar las llamadas HTTP por eventos mediante RabbitMQ o Kafka.
- **Service discovery**: Introducir herramientas como Consul o Eureka.
- **Rate limiting y seguridad avanzada**: Implementar OAuth2 o JWT.
- **Caching**: Redis para productos leídos con frecuencia.
- **Monitoring**: Incorporar Prometheus y Grafana.