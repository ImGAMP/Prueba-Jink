# Microservicio de Productos - Spring Boot + PostgreSQL

Este microservicio forma parte de un sistema distribuido orientado a la gestión de productos. Permite registrar, consultar, actualizar y eliminar productos, cumpliendo con buenas prácticas de arquitectura y pruebas automatizadas.

## Tecnologías utilizadas

- Java 17
- Spring Boot 3.4.4
- PostgreSQL
- Spring Data JPA
- Spring Validation
- Spring Boot Actuator
- Swagger OpenAPI
- Docker y Docker Compose
- JUnit 5 + Mockito + JaCoCo

## Estructura del proyecto

```
producto/
├── src/
│   ├── main/
│   │   ├── java/com/productos/
│   │   │   ├── controller/          # Controladores REST
│   │   │   ├── service/             # Lógica de negocio
│   │   │   ├── repository/          # Repositorio JPA
│   │   │   ├── dto/                 # Objetos de transferencia
│   │   │   ├── entity/              # Entidades JPA
│   │   │   ├── config/              # Filtros, Swagger y configuración
│   │   │   ├── exception/           # Manejo global de errores
│   │   │   └── api/                 # Envoltorio JSON:API
│   ├── test/
│   │   ├── unit/                    # Pruebas unitarias
│   │   └── integration/             # Pruebas de integración
├── application.yml                 # Configuración general
├── application-docker.yml         # Configuración para entorno dockerizado
├── Dockerfile                     # Imagen del microservicio
├── compose.yaml                   # Entorno local con Docker Compose
└── pom.xml                        # Dependencias Maven
```

## Instalación y ejecución local

1. Clonar el repositorio y acceder a la carpeta:

```bash
git clone https://github.com/tu_usuario/producto-service.git
cd producto
```

2. Compilar y ejecutar el proyecto:

```bash
./mvnw clean spring-boot:run
```

3. Acceder a la documentación Swagger:

http://localhost:8080/swagger-ui.html

## Docker y PostgreSQL

Para ejecutar todo el entorno usando Docker:

```bash
docker-compose -f compose.yaml up --build
```

## Seguridad

Este microservicio utiliza autenticación por API Key.  
Debes incluir el siguiente encabezado en cada solicitud:

```text
X-API-KEY: XYZ123
```

## Monitoreo

Se encuentra habilitado el módulo Spring Boot Actuator:

- Health check: `/actuator/health`
- Info: `/actuator/info`
- Métricas: `/actuator/metrics`

## Ejecución de pruebas

### Unitarias y de integración:

```bash
./mvnw test
```

### Cobertura con JaCoCo:

```bash
./mvnw jacoco:report
```

Abrir reporte HTML en:

```bash
target/site/jacoco/index.html
```

## Endpoints principales

| Método | Ruta              | Descripción                         |
|--------|-------------------|-------------------------------------|
| GET    | /productos        | Listar productos paginados          |
| GET    | /productos/{id}   | Obtener un producto por ID          |
| POST   | /productos        | Crear un nuevo producto             |
| PUT    | /productos/{id}   | Actualizar un producto existente    |
| DELETE | /productos/{id}   | Eliminar un producto por ID         |

## Consideraciones

- Implementa patrón JSON:API en las respuestas.
- Usa filtros para trazabilidad (`CorrelationId`) y validación de claves (`ApiKeyFilter`).
- Cobertura de pruebas mayor al 93%.
- Sistema desacoplado y preparado para escalar horizontalmente.

## Autor

Desarrollado por Gustavo Adolfo Mojica Perdigon  
Correo: gmojica@unal.edu.co  
2025


