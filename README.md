# 🚀 ReconBot - Herramienta de Hacking Ético

**ReconBot** es una aplicación avanzada de hacking ético que implementa técnicas de OSINT (Inteligencia de Fuentes Abiertas) utilizando Python, Django, DNS, Nmap, Whois y contenedores Docker.

## 🌟 Características Principales
- 🔍 Análisis avanzado de dominios (DNS, Whois)
- 📊 Integración con herramientas de escaneo (Nmap)
- 🐳 Despliegue simplificado con Docker
- 📡 Recopilación automatizada de información (OSINT)
- 🔐 Seguridad integrada para pruebas éticas

## 📋 Requisitos Previos

| Requisito | Versión Recomendada | Instalación |
|-----------|---------------------|-------------|
| Docker | 20.10+ | [Guía Oficial](https://docs.docker.com/get-docker/) |
| Docker Compose | 2.5+ | [Instrucciones](https://docs.docker.com/compose/install/) |
| Git | 2.35+ | `sudo apt install git` |

## 🛠️ Instalación Paso a Paso

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tuusuario/ReconBot.git
cd ReconBot
```
### 2. Configuración Inicial
```bash
# Preparar base de datos SQLite
touch db.sqlite3
chmod a+w db.sqlite3
touch .env
```
### 3. Configuracion de las variables de entorno
```env
DEEPSEEK_API_KEY=
API_KEY_SEARCH_GOOGLE=
SEARCH_ENGINE_ID=
```
[Consigue la clave de deepseek api](https://openrouter.ai/)
[Consigue las claves de busqueda en google](https://developers.google.com/custom-search/v1/overview)

### 4. Construir y desplegas
```bash
# Construir imágenes Docker
docker-compose build

# Iniciar servicios en segundo plano
docker-compose up -d

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario (opcional)
docker-compose exec web python manage.py createsuperuser
```

## Modulos Diponibles
1. Analisis WHOIS
```py
from reconbot.modules import whois_analysis
result = whois_analysis.run("ejemplo.com")
```
2. Escaneo DNS
```py
from reconbot.modules import dns_scan
records = dns_scan.run("ejemplo.com", record_types=['A', 'MX', 'TXT'])
```
3. Escaneo con NMAP
```py
# Ejemplo de comando Nmap integrado
docker-compose exec reconbot nmap -sV ejemplo.com
```
