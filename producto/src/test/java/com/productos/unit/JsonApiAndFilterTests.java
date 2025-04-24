package com.productos.unit;

import com.productos.api.JsonApiResponse;
import com.productos.api.JsonApiResponse.JsonApiData;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class JsonApiAndFilterTests {

    @Test
    void testWrapOneWithNullId() {
        String type = "test";
        Object attr = Map.of("key", "value");

        Map<String, Object> wrapped = JsonApiResponse.wrapOne(type, null, attr);
        JsonApiData<?> data = (JsonApiData<?>) wrapped.get("data");

        assertEquals("test", data.getType());
        assertNull(data.getId());
        assertEquals("value", ((Map<?, ?>) data.getAttributes()).get("key"));
    }

    @Test
    void testWrapListWithEmptyList() {
        Map<String, Object> wrapped = JsonApiResponse.wrapList("test", List.of());
        List<?> dataList = (List<?>) wrapped.get("data");

        assertNotNull(dataList);
        assertTrue(dataList.isEmpty());
    }

    @Test
    void testJsonApiDataWithNullId() {
        JsonApiData<String> data = new JsonApiData<>("test", null, "payload");
        assertEquals("test", data.getType());
        assertNull(data.getId());
        assertEquals("payload", data.getAttributes());
    }

}

