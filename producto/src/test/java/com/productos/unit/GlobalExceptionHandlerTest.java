package com.productos.unit;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import com.productos.exception.*;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

@SuppressWarnings("null")
public class GlobalExceptionHandlerTest {

    
    @Test
    void testHandleProductoNotFound() {
        ProductoNotFoundException ex = new ProductoNotFoundException("No encontrado");
        ResponseEntity<Map<String, Object>> response = new GlobalExceptionHandler().handleProductoNotFound(ex);
        assertEquals(404, response.getStatusCode().value());
        assertTrue(response.getBody().containsKey("errors"));
    }

    @Test
    void testHandleUnexpectedErrors() {
        Exception ex = new RuntimeException("Error");
        ResponseEntity<Map<String, Object>> response = new GlobalExceptionHandler().handleUnexpectedErrors(ex);
        assertEquals(500, response.getStatusCode().value());
        assertTrue(response.getBody().containsKey("errors"));
    }
}
