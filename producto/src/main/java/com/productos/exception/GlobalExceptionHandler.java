package com.productos.exception;

import org.springframework.http.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidationErrors(MethodArgumentNotValidException ex) {
        List<Map<String, Object>> errors = new ArrayList<>();

        ex.getBindingResult().getFieldErrors().forEach(error -> {
            Map<String, Object> errorObject = new HashMap<>();
            errorObject.put("status", "400");
            errorObject.put("title", "Campo inválido");
            errorObject.put("detail", error.getDefaultMessage());
            errorObject.put("source", Map.of("pointer", "/data/attributes/" + error.getField()));
            errors.add(errorObject);
        });

        return new ResponseEntity<>(Map.of("errors", errors), HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(ProductoNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleProductoNotFound(ProductoNotFoundException ex) {
        Map<String, Object> errorObject = new HashMap<>();
        errorObject.put("status", "404");
        errorObject.put("title", "Producto no encontrado");
        errorObject.put("detail", ex.getMessage());

        return new ResponseEntity<>(Map.of("errors", List.of(errorObject)), HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleUnexpectedErrors(Exception ex) {
        Map<String, Object> errorObject = new HashMap<>();
        errorObject.put("status", "500");
        errorObject.put("title", "Error inesperado");
        errorObject.put("detail", ex.getMessage());

        return new ResponseEntity<>(Map.of("errors", List.of(errorObject)), HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
