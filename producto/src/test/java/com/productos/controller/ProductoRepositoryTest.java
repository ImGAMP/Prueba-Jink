package com.productos.controller;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.math.BigDecimal;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.productos.entity.Producto;
import com.productos.repository.ProductoRepository;

@SpringBootTest
public class ProductoRepositoryTest {

    @Autowired
    private ProductoRepository repo;

    @Test
    public void debeGuardarUnProducto() {
        Producto p = new Producto(null, "Test", new BigDecimal("99.99"));
        Producto guardado = repo.save(p);
        assertNotNull(guardado.getId());
    }
}

