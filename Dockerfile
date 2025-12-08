FROM python:3.13.2-alpine3.21

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Para que Python no genere .pyc y loguee en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto dentro de la imagen
COPY . .

# Puerto interno donde escucha tu app (app.run(..., port=5000))
EXPOSE 5000

# Comando para arrancar el CRUD de recetario
CMD ["python", "app.py"]