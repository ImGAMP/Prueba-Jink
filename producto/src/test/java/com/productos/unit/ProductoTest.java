package com.productos.unit;

import org.junit.jupiter.api.Test;

import com.productos.entity.Producto;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;

public class ProductoTest {

    @Test
    void testConstructoresYGettersSetters() {
        Producto producto = new Producto();
        producto.setId(1L);
        producto.setNombre("Producto Uno");
        producto.setPrecio(new BigDecimal("500.00"));

        assertEquals(1L, producto.getId());
        assertEquals("Producto Uno", producto.getNombre());
        assertEquals(new BigDecimal("500.00"), producto.getPrecio());

        Producto producto2 = new Producto(2L, "Producto Dos", new BigDecimal("1000.00"));
        assertEquals(2L, producto2.getId());
        assertEquals("Producto Dos", producto2.getNombre());
        assertEquals(new BigDecimal("1000.00"), producto2.getPrecio());
    }

    @Test
    void testToString() {
        Producto producto = new Producto(3L, "Producto ToString", new BigDecimal("300.00"));
        String result = producto.toString();
        assertTrue(result.contains("Producto ToString"));
        assertTrue(result.contains("300.00"));
    }
}
