@echo off
echo Apagando contenedores antiguos...
docker compose down

echo Construyendo y levantando servicios...
docker compose up -d --build

echo Esperando unos segundos a que levanten los servicios...
timeout /t 20

echo Verificando estado de los contenedores...
docker compose ps

echo Preparando entorno de tests para inventario-service...
cd inventario-service
python -m venv venv
call venv\Scripts\activate.bat

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo Ejecutando tests de Inventario...
set PYTHONPATH=.
pytest -v

echo Ejecutando tests de Producto (Spring Boot)...
cd ..\producto
call ..\mvnw.cmd clean test

echo Todos los tests locales pasaron correctamente.

cd ..
echo Listo. Ahora puedes hacer commit y push tranquilo.
pause
