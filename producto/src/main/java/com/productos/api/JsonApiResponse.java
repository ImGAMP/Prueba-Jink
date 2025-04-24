package com.productos.api;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class JsonApiResponse {

    public static <T> Map<String, Object> wrapOne(String type, Long id, T attributes) {
        return Map.of(
            "data", new JsonApiData<>(type, id, attributes)
        );
    }

    public static <T> Map<String, Object> wrapList(String type, List<Item<T>> items) {
        List<JsonApiData<T>> dataList = items.stream()
                .map(item -> new JsonApiData<>(type, item.id(), item.attributes()))
                .collect(Collectors.toList());
        return Map.of("data", dataList);
    }

    public record Item<T>(Long id, T attributes) {}

    public static class JsonApiData<T> {
        private final String type;
        private final String id;
        private final T attributes;

        public JsonApiData(String type, Long id, T attributes) {
            this.type = type;
            this.id = id != null ? id.toString() : null;
            this.attributes = attributes;
        }

        public String getType() {
            return type;
        }

        public String getId() {
            return id;
        }

        public T getAttributes() {
            return attributes;
        }
    }
}