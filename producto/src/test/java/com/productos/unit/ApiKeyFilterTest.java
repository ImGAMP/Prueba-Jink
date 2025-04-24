package com.productos.unit;

import jakarta.servlet.FilterChain;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.junit.jupiter.api.Test;

import com.productos.config.ApiKeyFilter;

import static org.mockito.Mockito.*;

public class ApiKeyFilterTest {

    @Test
    void testDoFilterWithValidKey() throws Exception {
        ApiKeyFilter filter = new ApiKeyFilter();
        HttpServletRequest req = mock(HttpServletRequest.class);
        HttpServletResponse res = mock(HttpServletResponse.class);
        FilterChain chain = mock(FilterChain.class);

        when(req.getHeader("X-API-KEY")).thenReturn("XYZ123");
        filter.doFilter(req, res, chain);

        verify(chain, times(1)).doFilter(req, res);
    }

    @Test
    void testDoFilterWithInvalidKey() throws Exception {
        ApiKeyFilter filter = new ApiKeyFilter();
        HttpServletRequest req = mock(HttpServletRequest.class);
        HttpServletResponse res = mock(HttpServletResponse.class);
        FilterChain chain = mock(FilterChain.class);

        when(req.getHeader("X-API-KEY")).thenReturn("INVALID");
        filter.doFilter(req, res, chain);

        verify(res).sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid API Key");
    }
}