# Usa la imagen oficial de Python
FROM python:3.11-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea y establece el directorio de trabajo
WORKDIR /app

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el proyecto
COPY . .

# Puerto expuesto
EXPOSE 8000

# Comando de inicio
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
