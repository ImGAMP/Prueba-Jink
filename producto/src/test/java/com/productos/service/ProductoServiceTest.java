package com.productos.service;

import com.productos.entity.Producto;
import com.productos.exception.ProductoNotFoundException;
import com.productos.repository.ProductoRepository;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.context.SpringBootTest;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@SpringBootTest
public class ProductoServiceTest {

    @Mock
    private ProductoRepository repository;

    @InjectMocks
    private ProductoService service;

    public ProductoServiceTest() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testCrearProducto() {
        Producto producto = new Producto();
        producto.setNombre("Prueba");
        producto.setPrecio(new BigDecimal("99.99"));

        when(repository.save(any())).thenReturn(producto);

        Producto creado = service.crear(producto);
        assertEquals("Prueba", creado.getNombre());
    }

    @Test
    void testObtenerProducto() {
        Producto producto = new Producto();
        producto.setId(1L);
        producto.setNombre("Producto Test");

        when(repository.findById(1L)).thenReturn(Optional.of(producto));

        Producto resultado = service.obtener(1L);
        assertEquals("Producto Test", resultado.getNombre());
    }

    @Test
    void testProductoNoEncontrado() {
        when(repository.findById(2L)).thenReturn(Optional.empty());
        assertThrows(ProductoNotFoundException.class, () -> service.obtener(2L));
    }

    @Test
    void testEliminarProductoNoExistente() {
        when(repository.existsById(99L)).thenReturn(false);
        assertThrows(ProductoNotFoundException.class, () -> service.eliminar(99L));
    }
}
