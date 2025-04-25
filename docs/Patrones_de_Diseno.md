
# Patrones de Diseño Usados

Este proyecto incorpora varios patrones de diseño ampliamente aceptados en el desarrollo de sistemas distribuidos y microservicios. A continuación, se describen los principales:

## 1. **Patrón API Gateway (a futuro)**

Aunque no está implementado aún, se prevé la incorporación de un API Gateway para canalizar el tráfico y simplificar la comunicación entre clientes y servicios, manejando autenticación, enrutamiento, y agregación de resultados.

## 2. **Patrón Service Registry (a futuro)**

Como propuesta para crecimiento, podría añadirse un Service Registry como Consul o Eureka que permita la localización dinámica de servicios.

## 3. **Patrón Proxy (aplicado en cliente HTTP)**

El microservicio de Inventario actúa como un cliente proxy al servicio de Productos usando el módulo `httpx` para realizar llamadas HTTP autenticadas.

## 4. **Patrón Repository (aplicado en Java)**

En el microservicio de Productos (Java/Spring Boot), se implementa el patrón Repository para encapsular la lógica de acceso a datos con `ProductoRepository`, separando la lógica de negocio de la persistencia.

## 5. **Patrón DTO (Data Transfer Object)**

Ambos microservicios usan DTOs para representar estructuras de datos transmitidas entre capas. En Java (`ProductoDTO`, `ProductoRequest`) y en Python (Pydantic models).

## 6. **Patrón Adapter (cliente de productos en inventario)**

`productos_client.py` funciona como un Adapter para traducir y encapsular la lógica de comunicación entre el microservicio de Inventario y Productos.

## 7. **Patrón Singleton (por configuración)**

Las conexiones a bases de datos (`inventario_collection`, MongoClient y DataSource en Spring) se instancian una vez por aplicación y son reutilizadas.

## 8. **Patrón Circuit Breaker (a futuro)**

Se sugiere añadir un patrón de Circuit Breaker con librerías como `resilience4j` en Java o `httpx_retry` con `tenacity` en Python para evitar fallos en cascada.

---

**Documentado por:** Gustavo Adolfo Mojica Perdigón  
**Correo:** gmojica@unal.edu.co  
**Año:** 2025
