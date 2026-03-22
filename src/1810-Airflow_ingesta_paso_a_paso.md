# Caso Práctico paso a paso

## ⚠️ Advertencia ⚠️
Las APIs de Pyhton de Airflow3 están cambiando.
Asegúrate de que estás usando Airflow3 y que la documentación que lees en la web (o ha leído tu LLM si haces _vibe coding_) coincide con tu versió de Airflow.

El DAG tendrá esta apariencia en el GUI de Airflow:

![Caso Práctico](images/dag_caso_practico.png)


# Estructura del fichero

El fichero con el DAG se ha creado a partir de una plantilla _boilerplate_ de Apache Airflow3.

Tiene estas secciones:
- Imports
- Configuración del DAG
- Python callables (funciones que usaremos)
- Definición del DAG
  - Definición de Operadores que usamos.
  - Orden de ejecución de los operadores 

Vamos a verlas paso a paso:

## Imports

```python

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator

# Si buscas en la documentación de Airflow te puede aparecer este import:
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# pero si lo importas, falla.
# Hay que usar este en su lugar (lo usan los tests de Airflow)
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

```

Estos imports proporcionan las herramientas necesarias para crear y configurar el DAG:
- `datetime` y `timedelta` permiten trabajar con fechas y duras
- `DAG` es la clase base para definir el flujo de trabajo
- [`PythonOperator`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html#airflow.operators.python.PythonOperator), [`BashOperator`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/bash/index.html#airflow.operators.bash.BashOperator) y [`SQLExecuteQueryOperator`](https://airflow.apache.org/docs/apache-airflow-providers-common-sql/stable/operators.html) permiten ejecutar tareas de Python, comandos bash y consultas SQL en bases de datos, respectivamente.

## Configuración del DAG

En Airflow quien desarrolla los dags es quien decide cuándo se ejecutan, y cómo.
En otros orquestadores es el administrador del sistema quien se encarga de esto.
```python
# ---------------------------  CONFIGURATION  --------------------------- #
# Modify these values to fit your project.
DAG_ID = "0001_Practica_ingesta"
DESCRIPTION = "Ingesta de datos en PB"
TAGS = ["inigo"]
MAX_RUNTIME_MINUTES = 10  # fail after N minutes if task still running
RETRY_ATTEMPTS = 0  # fail fast during dev, increase in prod
RETRY_DELAY_MINUTES = 2
# -------------------------------------------------------------------------- #
```


## Python callables (funciones que usaremos)


##Definición del DAG
## Definición de Operadores que usamos.

## Flujo de tareas

Si no especificamos el flujo de tareas, Airflow ejecutará linealmente una tras otra las tareas que definamos.

Si tenemos un flujo mas complejo o queremos paralelizar ejecución de tareas (siempre que tengamos runners disponibles), tenemos que definir un flujo de esta manera:

```python
# ---------------------------  TASK FLOW  ------------------------- #

    copia_ficheros_entrantes >> leer_ficheros
    leer_ficheros >> insert_into_staging
    leer_ficheros >> borrar_ficheros_entrantes
    insert_into_staging >> borrar_ficheros_staging
    insert_into_staging >> insert_into_prod
    insert_into_prod >> truncate_staging

# ----------------------------------------------------------------------- #
```

Hay que tener cuidado cuando borramos datos con estas dos cosas:
- Condiciones de carrera
- Tener que volver a ir al transaccional a cargar datos sin necesidad.

Una condición de carrera se da cuando una operación depende del momento en que se ejecuta y puede producir resultados incorrectos si otros procesos modifican el estado entre la comprobación y la acción.

Por ejemplo, si usamos `rm *.csv` para borrar los ficheros que ya hemos procesado, pero mientras tanto siguen llegando nuevos ficheros al directorio, podemos acabar borrando ficheros que aún no hemos procesado, ya que el comando borrará todos los archivos CSV existentes en ese momento sin distinguir entre los procesados y los nuevos.

También puede ocurrir que borremos los ficheros "demasiado pronto" y en caso de que nuestro proceso falle total o parcialmente tengamos que volver al transaccional a descargar toda la información de nuevo en vez de descargar únicamente los últimos datos que necesitamos. 

Tenemos que tener en cuenta que no siempre podremos acceder a los datos del transaccional de nuevo, o que podemos tener una ventana temporal de acceso a esos sistemas que no podemos sobrepasar.
