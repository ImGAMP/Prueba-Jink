FROM eclipse-temurin:17-jdk-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar dependencias y código fuente
COPY target/producto-0.0.1-SNAPSHOT.jar app.jar

# Puerto de exposición (opcional)
EXPOSE 8080

# Variable de entorno para la JVM
ENV JAVA_OPTS="-Xms128m -Xmx512m"

# Comando de inicio
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]