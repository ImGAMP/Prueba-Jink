package com.productos.unit;

import static org.junit.jupiter.api.Assertions.*;

import java.math.BigDecimal;
import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.TestPropertySource;

import com.productos.entity.Producto;
import com.productos.repository.ProductoRepository;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@TestPropertySource(properties = {
    "spring.jpa.hibernate.ddl-auto=create-drop",
    "spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=PostgreSQL"
})
public class ProductoRepositoryTest {

    @Autowired
    private ProductoRepository productoRepository;

    @Test
    public void debeGuardarYRecuperarProducto() {
        // Arrange
        Producto producto = new Producto(null, "Laptop", new BigDecimal("1299.99"));
        
        // Act
        Producto guardado = productoRepository.save(producto);
        Optional<Producto> encontrado = productoRepository.findById(guardado.getId());
        
        // Assert
        assertAll(
            () -> assertNotNull(guardado.getId(), "El ID no debería ser nulo después de guardar"),
            () -> assertTrue(encontrado.isPresent(), "Debería encontrar el producto guardado"),
            () -> assertEquals("Laptop", encontrado.get().getNombre(), "El nombre no coincide"),
            () -> assertEquals(0, new BigDecimal("1299.99").compareTo(encontrado.get().getPrecio()), 
                "El precio no coincide")
        );
    }

    @Test
    public void debeEncontrarProductoPorNombre() {
        // Arrange
        Producto producto = productoRepository.save(
            new Producto(null, "Teclado", new BigDecimal("59.99")));
        
        // Act
        Optional<Producto> resultado = productoRepository.findByNombre("Teclado");
        
        // Assert
        assertTrue(resultado.isPresent());
        assertEquals(producto.getId(), resultado.get().getId());
    }
}
