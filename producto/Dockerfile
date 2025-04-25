# Imagen con Maven y JDK 17
FROM maven:3.9.6-eclipse-temurin-17

# Crear directorio de trabajo
WORKDIR /app

# Copiar el código fuente
COPY . .

# Exponer el puerto
EXPOSE 8080

# Ejecutar con spring-boot:run
CMD ["mvn", "spring-boot:run"]
