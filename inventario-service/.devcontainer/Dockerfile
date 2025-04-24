# Imagen base oficial
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del microservicio al contenedor
COPY . .

# Crear y activar entorno virtual (opcional en slim, pero buena práctica)
ENV VIRTUAL_ENV=/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto (de acuerdo a uvicorn)
EXPOSE 8000

# Comando de ejecución
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
