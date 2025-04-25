package com.productos.controller;

import com.productos.api.JsonApiResponse;
import com.productos.dto.ProductoDTO;
import com.productos.dto.ProductoRequest;
import com.productos.entity.Producto;
import com.productos.service.ProductoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@Validated
@RequestMapping("/productos")
@Tag(name = "Productos", description = "Operaciones CRUD sobre productos")
public class ProductoController {

    private static final Logger logger = LoggerFactory.getLogger(ProductoController.class);

    @Autowired
    private ProductoService service;

    @GetMapping("/saludo")
    public String saludo() {
        return "Hola, mundo actualizado!";
    }

    @Operation(summary = "Crear un producto")
    @PostMapping
    public Object crear(@Valid @RequestBody ProductoRequest request) {
        logger.info("Solicitud de creación de producto recibida. CorrelationId: {}, nombre: {}, precio: {}",
                MDC.get("correlationId"), request.getNombre(), request.getPrecio());

        Producto producto = new Producto();
        producto.setNombre(request.getNombre());
        producto.setPrecio(request.getPrecio());

        Producto creado = service.crear(producto);
        ProductoDTO dto = new ProductoDTO(creado.getId(), creado.getNombre(), creado.getPrecio());

        logger.info("Producto creado con éxito. ID: {}, CorrelationId: {}", dto.getId(), MDC.get("correlationId"));
        return JsonApiResponse.wrapOne("productos", dto.getId(), dto);
    }

    @Operation(summary = "Obtener un producto por ID")
    @GetMapping("/{id}")
    public Object obtener(@PathVariable Long id) {
        logger.info("Solicitud para obtener producto con ID: {}. CorrelationId: {}", id, MDC.get("correlationId"));

        Producto producto = service.obtener(id);
        ProductoDTO dto = new ProductoDTO(producto.getId(), producto.getNombre(), producto.getPrecio());

        logger.info("Producto obtenido correctamente. ID: {}, CorrelationId: {}", dto.getId(),
                MDC.get("correlationId"));
        return JsonApiResponse.wrapOne("productos", dto.getId(), dto);
    }

    @Operation(summary = "Actualizar un producto por ID")
    @PutMapping("/{id}")
    public Object actualizar(@PathVariable Long id, @Valid @RequestBody ProductoRequest request) {
        logger.info(
                "Solicitud de actualización de producto con ID: {}. CorrelationId: {}, nuevos datos -> nombre: {}, precio: {}",
                id, MDC.get("correlationId"), request.getNombre(), request.getPrecio());

        Producto producto = new Producto();
        producto.setNombre(request.getNombre());
        producto.setPrecio(request.getPrecio());

        Producto actualizado = service.actualizar(id, producto);
        ProductoDTO dto = new ProductoDTO(actualizado.getId(), actualizado.getNombre(), actualizado.getPrecio());

        logger.info("Producto actualizado exitosamente. ID: {}, CorrelationId: {}", dto.getId(),
                MDC.get("correlationId"));
        return JsonApiResponse.wrapOne("productos", dto.getId(), dto);
    }

    @Operation(summary = "Eliminar un producto por ID")
    @DeleteMapping("/{id}")
    public void eliminar(@PathVariable Long id) {
        logger.warn("Solicitud para eliminar producto. ID: {}, CorrelationId: {}", id, MDC.get("correlationId"));
        service.eliminar(id);
        logger.info("Producto eliminado correctamente. ID: {}, CorrelationId: {}", id, MDC.get("correlationId"));
    }

    @Operation(summary = "Listar productos con paginación")
    @GetMapping
    public Object listar(@RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        logger.info("Solicitud para listar productos. Página: {}, Tamaño: {}, CorrelationId: {}",
                page, size, MDC.get("correlationId"));

        List<JsonApiResponse.Item<ProductoDTO>> items = service.listar(page, size)
                .stream()
                .map(p -> new ProductoDTO(p.getId(), p.getNombre(), p.getPrecio()))
                .map(dto -> new JsonApiResponse.Item<>(dto.getId(), dto))
                .collect(Collectors.toList());

        logger.info("Se listaron {} productos. CorrelationId: {}", items.size(), MDC.get("correlationId"));
        return JsonApiResponse.wrapList("productos", items);
    }
}
