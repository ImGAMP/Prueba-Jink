package com.productos.unit;

import org.junit.jupiter.api.Test;

import com.productos.api.JsonApiResponse;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class JsonApiResponseTest {

    @Test
    void testWrapOne() {
        var data = JsonApiResponse.wrapOne("productos", 1L, Map.of("nombre", "Test"));
        assertNotNull(data);
        assertTrue(data.containsKey("data"));
        var response = (JsonApiResponse.JsonApiData<?>) data.get("data");
        assertEquals("productos", response.getType());
        assertEquals("1", response.getId());
        assertEquals("Test", ((Map<?, ?>) response.getAttributes()).get("nombre"));
    }

    @Test
    void testWrapList() {
        var items = List.of(new JsonApiResponse.Item<>(1L, Map.of("nombre", "Test1")),
                            new JsonApiResponse.Item<>(2L, Map.of("nombre", "Test2")));
        var data = JsonApiResponse.wrapList("productos", items);
        assertNotNull(data);
        assertTrue(data.containsKey("data"));
        List<?> dataList = (List<?>) data.get("data");
        assertEquals(2, dataList.size());
    }
}