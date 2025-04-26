# Makefile para gestión de servicios y tests

.PHONY: help test setup build up down logs clean

# Mostrar ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make setup    - Configurar entorno virtual e instalar dependencias"
	@echo "  make test     - Ejecutar tests de Python"
	@echo "  make build    - Construir contenedores Docker"
	@echo "  make up       - Levantar contenedores"
	@echo "  make down     - Apagar contenedores"
	@echo "  make logs     - Ver logs de contenedores"
	@echo "  make clean    - Limpiar entorno virtual y contenedores"

# Crear entorno virtual e instalar dependencias
setup:
	@echo "Configurando entorno virtual..."
	@if [ ! -d "./inventario-service/venv" ]; then \
		cd inventario-service && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt; \
	else \
		echo "Entorno virtual ya existe."; \
	fi

# Ejecutar tests de inventario-service
test: setup
	@echo "Ejecutando tests de Python..."
	cd inventario-service && source venv/bin/activate && pytest

# Construir imágenes Docker
build:
	@echo "Construyendo imágenes Docker..."
	docker compose build

# Levantar servicios
up:
	@echo "Levantando servicios..."
	docker compose up -d

# Apagar servicios
down:
	@echo "Apagando servicios..."
	docker compose down

# Ver logs de todos los contenedores
logs:
	@echo "Mostrando logs..."
	docker compose logs -f --tail=100

# Limpiar entorno: eliminar venv y bajar contenedores
clean:
	@echo "Limpiando entorno..."
	docker compose down
	@rm -rf inventario-service/venv
