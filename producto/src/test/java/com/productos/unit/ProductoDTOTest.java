package com.productos.unit;

import org.junit.jupiter.api.Test;

import com.productos.dto.ProductoDTO;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;

public class ProductoDTOTest {

    @Test
    void testConstructoresYGettersSetters() {
        ProductoDTO dto = new ProductoDTO();
        dto.setId(1L);
        dto.setNombre("Producto Test");
        dto.setPrecio(new BigDecimal("100.00"));

        assertEquals(1L, dto.getId());
        assertEquals("Producto Test", dto.getNombre());
        assertEquals(new BigDecimal("100.00"), dto.getPrecio());

        ProductoDTO dto2 = new ProductoDTO(2L, "Otro Producto", new BigDecimal("200.00"));
        assertEquals(2L, dto2.getId());
        assertEquals("Otro Producto", dto2.getNombre());
        assertEquals(new BigDecimal("200.00"), dto2.getPrecio());
    }
}
