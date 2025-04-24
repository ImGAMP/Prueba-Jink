package com.productos.unit;

import com.productos.entity.Producto;
import com.productos.exception.ProductoNotFoundException;
import com.productos.repository.ProductoRepository;
import com.productos.service.ProductoService;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class ProductoServiceTest {

    @Mock
    private ProductoRepository repository;

    @InjectMocks
    private ProductoService service;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testCrearProducto() {
        Producto producto = new Producto(null, "Prueba", new BigDecimal("99.99"));
        when(repository.save(any())).thenReturn(producto);

        Producto creado = service.crear(producto);
        assertEquals("Prueba", creado.getNombre());
        verify(repository).save(producto);
    }

    @Test
    void testObtenerProducto() {
        Producto producto = new Producto(1L, "Producto Test", new BigDecimal("100.00"));
        when(repository.findById(1L)).thenReturn(Optional.of(producto));

        Producto resultado = service.obtener(1L);
        assertEquals("Producto Test", resultado.getNombre());
        verify(repository).findById(1L);
    }

    @Test
    void testProductoNoEncontrado() {
        when(repository.findById(2L)).thenReturn(Optional.empty());
        assertThrows(ProductoNotFoundException.class, () -> service.obtener(2L));
    }

    @Test
    void testActualizarProductoExistente() {
        Producto producto = new Producto(null, "Nuevo Nombre", new BigDecimal("123.45"));

        when(repository.existsById(1L)).thenReturn(true);
        when(repository.save(any())).thenAnswer(inv -> {
            Producto p = inv.getArgument(0);
            p.setId(1L);
            return p;
        });

        Producto actualizado = service.actualizar(1L, producto);
        assertEquals(1L, actualizado.getId());
        assertEquals("Nuevo Nombre", actualizado.getNombre());
        verify(repository).save(producto);
    }

    @Test
    void testActualizarProductoNoExistente() {
        Producto producto = new Producto(null, "X", BigDecimal.ONE);
        when(repository.existsById(9L)).thenReturn(false);

        assertThrows(ProductoNotFoundException.class, () -> service.actualizar(9L, producto));
    }

    @Test
    void testEliminarProductoExistente() {
        when(repository.existsById(1L)).thenReturn(true);
        doNothing().when(repository).deleteById(1L);

        service.eliminar(1L);
        verify(repository).deleteById(1L);
    }

    @Test
    void testEliminarProductoNoExistente() {
        when(repository.existsById(99L)).thenReturn(false);
        assertThrows(ProductoNotFoundException.class, () -> service.eliminar(99L));
    }
}
