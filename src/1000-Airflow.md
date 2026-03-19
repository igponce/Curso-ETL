# ETL con Airflow

## Conociendo Airflow
- ¿Qué es Airflow?
  - Planficador de jobs
  - Lo importante de un planificador es..
- Directed Acyclic Graphs (DAG)
  - Mismo concepto que en Spark
  - Diferencia: los JOBs

## Airflow "por dentro"
- Estructura directorios (dónde está lo mío)
- Conexiónes y credenciales
  - Separadas del código
  - Se almacenan en la BBDD (Postgres o sqlite)
- Nuestro primer DAG
  - Operadores
  - Sensores
  - Acciones

## Operadores de uso común

- SQL
- dbt
-

## XCOM - Comunicación entre Operadores


## Pitfalls

- Interfaz de usuario
  - ¿Dónde puedo hacer cosas?

- Inicio de los jobs
  - 'start_date': days_ago(1) ¿para ayer?

- Renombrado de DAGs
  - No se renombran los dags.
  - Se pueden renombrar *pero* no se hace.

  - Práctica renombrado
    - Crear un dag
    - Ejecutarlo varias veces
    - Renombramos el dag
    
## Buenas prácticas

- Python Operator
  - Crea tu propio container para ejecutar tu código.
  - Te evita tener que instalar las dependencias de tu DAG en Python.

# Ejemplo de dags

## Ejemplo 1: Data Warehouse - carga de datos raw

## Ejemplo 2: Carga de datos en BBDD de productos

```mermaid

p p p 
```
