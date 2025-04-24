package com.productos.integration;

import com.fasterxml.jackson.databind.JsonNode;
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
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
public class ProductoCommunicationIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ProductoRepository productoRepository;

    @Autowired
    private ObjectMapper objectMapper;

    private Long productoId;

    @BeforeEach
    void setUp() {
        productoRepository.deleteAll();
        Producto producto = new Producto(null, "Disco SSD", new BigDecimal("340000"));
        productoId = productoRepository.save(producto).getId();
    }

    @Test
    void debeObtenerProductoEnFormatoJsonApi() throws Exception {
        mockMvc.perform(get("/productos/" + productoId)
                        .header("X-API-KEY", "XYZ123")
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.type", is("productos")))
                .andExpect(jsonPath("$.data.id", is(productoId.toString())))
                .andExpect(jsonPath("$.data.attributes.nombre", is("Disco SSD")))
                .andExpect(jsonPath("$.data.attributes.precio", is(closeTo(340000.0, 0.01))));
    }

    @Test
    void debeRetornar404SiProductoNoExisteParaInventario() throws Exception {
        mockMvc.perform(get("/productos/999999")
                        .header("X-API-KEY", "XYZ123")
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound());
    }

    @Test
    void debeTenerFormatoJsonApiCompleto() throws Exception {
        String response = mockMvc.perform(get("/productos/" + productoId)
                        .header("X-API-KEY", "XYZ123")
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andReturn()
                .getResponse()
                .getContentAsString();

        JsonNode root = objectMapper.readTree(response);
        assertTrue(root.has("data"));
        assertTrue(root.get("data").has("id"));
        assertTrue(root.get("data").has("type"));
        assertTrue(root.get("data").has("attributes"));
        assertTrue(root.get("data").get("attributes").has("nombre"));
        assertTrue(root.get("data").get("attributes").has("precio"));
    }

    @Test
    void debeResponderConJsonCorrectoParaOtroServicio() throws Exception {
        String response = mockMvc.perform(get("/productos/" + productoId)
                        .header("X-API-KEY", "XYZ123")
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andReturn()
                .getResponse()
                .getContentAsString();

        JsonNode producto = objectMapper.readTree(response).get("data");
        assertEquals("productos", producto.get("type").asText());
        assertEquals(productoId.toString(), producto.get("id").asText());
        assertNotNull(producto.get("attributes").get("nombre"));
        assertNotNull(producto.get("attributes").get("precio"));
    }
}
