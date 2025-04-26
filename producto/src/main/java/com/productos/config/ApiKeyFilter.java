package com.productos.config;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import java.io.IOException;

@Component
@Profile("!test") // Se activa en todos los entornos excepto en pruebas
public class ApiKeyFilter implements Filter {

    @Value("${app.api-key:XYZ123}") // Aquí se carga la API_KEY desde propiedades o entorno
    private String expectedApiKey;

    private static final String API_KEY_HEADER = "X-API-KEY";

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        String path = req.getRequestURI();

        // Permitir acceso sin API Key a health, info y saludo
        if (path.startsWith("/actuator/health") || path.startsWith("/actuator/info") || path.startsWith("/productos/saludo")) {
            chain.doFilter(request, response);
            return;
        }

        String apiKey = req.getHeader(API_KEY_HEADER);

        if (!expectedApiKey.equals(apiKey)) {
            ((HttpServletResponse) response).sendError(HttpServletResponse.SC_FORBIDDEN, "Forbidden: API Key inválida");
            return;
        }

        chain.doFilter(request, response);
    }
}

