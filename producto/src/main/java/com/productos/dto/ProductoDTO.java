package com.productos.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import java.math.BigDecimal;

public class ProductoDTO {

    private Long id;

    @NotBlank(message = "El nombre no puede estar vacío")
    private String nombre;

    @DecimalMin(value = "0.0", inclusive = false, message = "El precio debe ser mayor a cero")
    private BigDecimal precio;

    public ProductoDTO() {}

    public ProductoDTO(Long id, String nombre, BigDecimal precio) {
        this.id = id;
        this.nombre = nombre;
        this.precio = precio;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public BigDecimal getPrecio() {
        return precio;
    }

    public void setPrecio(BigDecimal precio) {
        this.precio = precio;
    }
}