package com.productos.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.productos.entity.Producto;
import com.productos.repository.ProductoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;

import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(classes = com.productos.ProductoApplication.class)
@ActiveProfiles("test")
@AutoConfigureMockMvc
public class ProductoIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ProductoRepository productoRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        productoRepository.deleteAll();
        productoRepository.save(new Producto(null, "Monitor LG", new BigDecimal("750000")));
        productoRepository.save(new Producto(null, "Teclado Logitech", new BigDecimal("125000")));
    }

    @Test
    void debeListarProductos() throws Exception {
        mockMvc.perform(get("/productos")
                .param("page", "0")
                .param("size", "10")
                .contentType(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$", hasSize(2)))
            .andExpect(jsonPath("$[0].nombre", is("Monitor LG")))
            .andExpect(jsonPath("$[1].nombre", is("Teclado Logitech")));
    }

    @Test
    void debeCrearProducto() throws Exception {
        var nuevoProducto = new com.productos.dto.ProductoDTO(null, "Mouse HP", new BigDecimal("89900"));

        mockMvc.perform(post("/productos")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(nuevoProducto)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id", notNullValue()))
            .andExpect(jsonPath("$.nombre", is("Mouse HP")))
            .andExpect(jsonPath("$.precio", is(89900)));
    }

    @Test
    void debeObtenerProductoPorId() throws Exception {
        Producto producto = productoRepository.save(new Producto(null, "Tablet Xiaomi", new BigDecimal("1200000")));

        mockMvc.perform(get("/productos/" + producto.getId())
                .contentType(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.nombre", is("Tablet Xiaomi")))
            .andExpect(jsonPath("$.precio", closeTo(1200000.0, 0.01)));
    }

    @Test
    void debeRetornar404SiProductoNoExiste() throws Exception {
        mockMvc.perform(get("/productos/9999")
                .contentType(MediaType.APPLICATION_JSON))
            .andExpect(status().isNotFound());
    }

    @Test
    void debeValidarCamposAlCrear() throws Exception {
        var productoInvalido = new com.productos.dto.ProductoDTO(null, "", new BigDecimal("0"));

        mockMvc.perform(post("/productos")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(productoInvalido)))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.errors", notNullValue()));
    }
}
