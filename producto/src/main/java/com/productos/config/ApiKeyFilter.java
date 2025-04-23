package com.productos.config;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import java.io.IOException;

@Component
@Profile("!test")
public class ApiKeyFilter implements Filter {

    private static final String API_KEY = "XYZ123";

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        String apiKey = req.getHeader("X-API-KEY");

        if (!API_KEY.equals(apiKey)) {
            ((HttpServletResponse) response).sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid API Key");
            return;
        }
        chain.doFilter(request, response);
    }
}

