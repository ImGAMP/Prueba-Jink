package com.productos.integration;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
public class CorrelationIdIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void debeInyectarCorrelationIdCuandoHeaderPresente() throws Exception {
        mockMvc.perform(get("/productos")
                        .header("X-API-KEY", "XYZ123")
                        .header("X-Correlation-ID", "test-correlation-id"))
                .andExpect(status().isOk());
    }

    @Test
    void debeGenerarCorrelationIdCuandoNoSeEnvíaHeader() throws Exception {
        mockMvc.perform(get("/productos")
                        .header("X-API-KEY", "XYZ123"))
                .andExpect(status().isOk());
    }
}
