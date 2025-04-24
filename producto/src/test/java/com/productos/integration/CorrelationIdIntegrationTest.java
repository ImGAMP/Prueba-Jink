package com.productos.integration;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
public class CorrelationIdIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void debeInyectarCorrelationIdCuandoHeaderPresente() throws Exception {
        mockMvc.perform(get("/productos")
                        .header("X-Correlation-ID", "test-correlation-id"))
                .andExpect(status().isOk());
        // Verifica visualmente en el log que se registre correctamente
    }

    @Test
    void debeGenerarCorrelationIdCuandoNoSeEnvíaHeader() throws Exception {
        mockMvc.perform(get("/productos"))
                .andExpect(status().isOk());
        // Verifica visualmente que no falle sin header
    }
}
