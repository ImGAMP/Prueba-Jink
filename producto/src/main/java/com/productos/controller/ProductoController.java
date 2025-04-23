package com.productos.controller;

import com.productos.dto.ProductoDTO;
import com.productos.entity.Producto;
import com.productos.service.ProductoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/productos")
@Tag(name = "Productos", description = "Operaciones CRUD sobre productos")
public class ProductoController {

    @Autowired
    private ProductoService service;

    @Operation(summary = "Crear un producto")
    @PostMapping
    public ProductoDTO crear(@Valid @RequestBody ProductoDTO dto) {
        Producto producto = new Producto();
        producto.setNombre(dto.getNombre());
        producto.setPrecio(dto.getPrecio());
        Producto creado = service.crear(producto);
        return new ProductoDTO(creado.getId(), creado.getNombre(), creado.getPrecio());
    }

    @Operation(summary = "Obtener un producto por ID")
    @GetMapping("/{id}")
    public ProductoDTO obtener(@PathVariable Long id) {
        Producto producto = service.obtener(id);
        return new ProductoDTO(producto.getId(), producto.getNombre(), producto.getPrecio());
    }

    @Operation(summary = "Actualizar un producto por ID")
    @PutMapping("/{id}")
    public ProductoDTO actualizar(@PathVariable Long id, @Valid @RequestBody ProductoDTO dto)  {
        Producto producto = new Producto();
        producto.setNombre(dto.getNombre());
        producto.setPrecio(dto.getPrecio());
        Producto actualizado = service.actualizar(id, producto);
        return new ProductoDTO(actualizado.getId(), actualizado.getNombre(), actualizado.getPrecio());
    }

    @Operation(summary = "Eliminar un producto por ID")
    @DeleteMapping("/{id}")
    public void eliminar(@PathVariable Long id) {
        service.eliminar(id);
    }

    @Operation(summary = "Listar productos con paginación")
    @GetMapping
    public List<ProductoDTO> listar(@RequestParam(defaultValue = "0") int page,
                                    @RequestParam(defaultValue = "10") int size) {
        return service.listar(page, size)
                .stream()
                .map(p -> new ProductoDTO(p.getId(), p.getNombre(), p.getPrecio()))
                .collect(Collectors.toList());
    }
}