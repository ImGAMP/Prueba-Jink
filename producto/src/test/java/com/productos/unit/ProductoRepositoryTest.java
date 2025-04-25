package com.productos.unit;

import static org.junit.jupiter.api.Assertions.*;

import java.math.BigDecimal;
import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import com.productos.entity.Producto;
import com.productos.repository.ProductoRepository;

@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@ActiveProfiles("test")
public class ProductoRepositoryTest {

    @Autowired
    private ProductoRepository productoRepository;

    @Test
    public void debeGuardarProductoCorrectamente() {
        // Arrange
        Producto producto = new Producto(null, "Monitor", new BigDecimal("299.99"));
        
        // Act
        Producto guardado = productoRepository.save(producto);
        
        // Assert
        assertNotNull(guardado.getId());
        assertEquals("Monitor", guardado.getNombre());
        assertEquals(0, new BigDecimal("299.99").compareTo(guardado.getPrecio()));
    }

    @Test
    public void debeEncontrarProductoPorNombre() {
        // Arrange
        productoRepository.save(new Producto(null, "Mouse", new BigDecimal("25.50")));
        
        // Act
        Optional<Producto> resultado = productoRepository.findByNombre("Mouse");
        
        // Assert
        assertTrue(resultado.isPresent());
        assertEquals("Mouse", resultado.get().getNombre());
    }

    @Test
    public void debeVerificarExistenciaPorNombre() {
        // Arrange
        productoRepository.save(new Producto(null, "Teclado", new BigDecimal("59.99")));
        
        // Act & Assert
        assertTrue(productoRepository.existsByNombre("Teclado"));
        assertFalse(productoRepository.existsByNombre("Inexistente"));
    }
}
