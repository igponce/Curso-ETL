# Laboratorio de Apache Airflow

Este directorio tiene lo necesario para instalar airflow en tu ordenador.

Para instalar airflow ejecuta:
```bash
uv sync # Todos los paquetes estan en uv.loc
```
Una vez instalado debes inicializar airflow:

```bash
uv run airflow init
```

Por último, ejecutamos airflow:
```bash
uv run airflow standalone
```
