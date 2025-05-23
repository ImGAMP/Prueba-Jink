package com.productos.config;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import java.io.IOException;

@Component
@Profile("!test") // Se activa en todos los entornos excepto pruebas
public class ApiKeyFilter implements Filter {

    private static final String API_KEY_HEADER = "X-API-KEY";
    private static final String EXPECTED_API_KEY;

    static {
        String envKey = System.getenv("API_KEY");
        EXPECTED_API_KEY = (envKey != null && !envKey.isBlank()) ? envKey : "XYZ123";
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        String path = req.getRequestURI();
        if (path != null && (path.startsWith("/actuator/health") || path.startsWith("/actuator/info") || path.startsWith("/productos/saludo"))) {
            chain.doFilter(request, response);
            return;
        }

        String apiKey = req.getHeader(API_KEY_HEADER);
        if (!EXPECTED_API_KEY.equals(apiKey)) {
            res.sendError(HttpServletResponse.SC_FORBIDDEN, "Forbidden: API Key inválida");
            return;
        }

        chain.doFilter(request, response);
    }
}



