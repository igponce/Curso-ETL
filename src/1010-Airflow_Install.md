# Instalar Airflow

Para hacer las prácticas necesitamos instalar airflow en nuestro equipo.

## Python

Seguimos las instrucciones de instalación de Apache-Airflow ***desde el directorio \lab **

1. Instalamos el paquete `apache-airflow`
Utilizando python, ejecutamos `uv add apache-airflow` (necesitamos tener uv de Ashral instalado previamente).

2. Inicializamos la base de datos de airflow

```bash
uv exec airflow init
```

3. Ejecutamos airflow

```bash
uv run airflow standalone
```
