package com.productos.controller;
import com.productos.dto.ProductoDTO;
import com.productos.entity.Producto;
import com.productos.service.ProductoService;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class ProductoControllerTest {

    @Mock
    private ProductoService service;

    @InjectMocks
    private ProductoController controller;

    public ProductoControllerTest() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testObtenerProductoPorId() {
        Producto producto = new Producto();
        producto.setId(1L);
        producto.setNombre("Producto Controller Test");
        producto.setPrecio(new BigDecimal("120.00"));

        when(service.obtener(1L)).thenReturn(producto);

        ProductoDTO dto = controller.obtener(1L);
        assertEquals("Producto Controller Test", dto.getNombre());
        assertEquals(new BigDecimal("120.00"), dto.getPrecio());
    }

    @Test
    void testCrearProducto() {
        ProductoDTO dto = new ProductoDTO(null, "Nuevo", new BigDecimal("150.00"));
        Producto producto = new Producto();
        producto.setId(1L);
        producto.setNombre("Nuevo");
        producto.setPrecio(new BigDecimal("150.00"));

        when(service.crear(any())).thenReturn(producto);

        ProductoDTO creado = controller.crear(dto);
        assertEquals("Nuevo", creado.getNombre());
        assertEquals(new BigDecimal("150.00"), creado.getPrecio());
    }
}