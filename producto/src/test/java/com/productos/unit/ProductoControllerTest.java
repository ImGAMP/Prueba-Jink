package com.productos.unit;

import com.productos.api.JsonApiResponse.JsonApiData;
import com.productos.controller.ProductoController;
import com.productos.dto.ProductoDTO;
import com.productos.dto.ProductoRequest;
import com.productos.entity.Producto;
import com.productos.exception.ProductoNotFoundException;
import com.productos.service.ProductoService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.domain.PageImpl;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class ProductoControllerTest {

    @Mock
    private ProductoService service;

    @InjectMocks
    private ProductoController controller;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testObtenerProductoPorId() {
        Producto producto = new Producto(1L, "Producto Controller Test", new BigDecimal("120.00"));
        when(service.obtener(1L)).thenReturn(producto);

        Object result = controller.obtener(1L);
        JsonApiData<?> data = (JsonApiData<?>) ((Map<?, ?>) result).get("data");

        assertEquals("productos", data.getType());
        assertEquals("1", data.getId());
        ProductoDTO dto = (ProductoDTO) data.getAttributes();
        assertEquals("Producto Controller Test", dto.getNombre());
        assertEquals(new BigDecimal("120.00"), dto.getPrecio());
    }

    @Test
    void testCrearProducto() {
        Producto producto = new Producto(1L, "Nuevo", new BigDecimal("150.00"));
        when(service.crear(any())).thenReturn(producto);

        ProductoRequest request = new ProductoRequest("Nuevo", new BigDecimal("150.00"));
        Object result = controller.crear(request);
        JsonApiData<?> data = (JsonApiData<?>) ((Map<?, ?>) result).get("data");

        assertEquals("productos", data.getType());
        assertEquals("1", data.getId());
        ProductoDTO dto = (ProductoDTO) data.getAttributes();
        assertEquals("Nuevo", dto.getNombre());
        assertEquals(new BigDecimal("150.00"), dto.getPrecio());
    }

    @Test
    void testActualizarProducto() {
        Producto productoActualizado = new Producto(1L, "Actualizado", new BigDecimal("199.99"));
        when(service.actualizar(eq(1L), any())).thenReturn(productoActualizado);

        ProductoRequest request = new ProductoRequest("Actualizado", new BigDecimal("199.99"));
        Object result = controller.actualizar(1L, request);
        JsonApiData<?> data = (JsonApiData<?>) ((Map<?, ?>) result).get("data");

        assertEquals("productos", data.getType());
        assertEquals("1", data.getId());
        ProductoDTO dto = (ProductoDTO) data.getAttributes();
        assertEquals("Actualizado", dto.getNombre());
        assertEquals(new BigDecimal("199.99"), dto.getPrecio());
    }

    @Test
    void testEliminarProducto() {
        doNothing().when(service).eliminar(1L);
        assertDoesNotThrow(() -> controller.eliminar(1L));
        verify(service, times(1)).eliminar(1L);
    }

    @Test
    void testProductoNoEncontrado() {
        when(service.obtener(99L)).thenThrow(new ProductoNotFoundException("No existe"));
        assertThrows(ProductoNotFoundException.class, () -> controller.obtener(99L));
    }

    @Test
    void testListarProductos() {
        List<Producto> productos = Arrays.asList(
                new Producto(1L, "Prod A", new BigDecimal("10.00")),
                new Producto(2L, "Prod B", new BigDecimal("20.00"))
        );
        when(service.listar(0, 10)).thenReturn(new PageImpl<>(productos));

        Object result = controller.listar(0, 10);
        List<?> dataList = (List<?>) ((Map<?, ?>) result).get("data");

        assertEquals(2, dataList.size());
        JsonApiData<?> data0 = (JsonApiData<?>) dataList.get(0);
        ProductoDTO dto = (ProductoDTO) data0.getAttributes();
        assertEquals("productos", data0.getType());
        assertEquals("1", data0.getId());
        assertEquals("Prod A", dto.getNombre());
    }
}
