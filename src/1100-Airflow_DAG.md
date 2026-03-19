
# DAGs en Airflow

## ¿Qué es un DAG?

Un **DAG** (Directed Acyclic Graph) es una estructura matemática compuesta por:
- **Nodos** (vértices): Representan tareas o procesos
- **Aristas dirigidas**: Conectan los nodos indicando dependencias y flujo de ejecución
- **Acíclico**: No permite ciclos (no puedes volver atrás a un nodo ya visitado)

Un DAG es un grafo que muestra cómo diferentes tareas dependen unas de otras, garantizando que las dependencias se resuelvan en el orden correcto.

## Cómo utiliza Apache Airflow los DAGs

El DAGs es el concepto central para definir flujos de trabajo de datos en Airflow:

## Definición de DAGs en Airflow
- Los DAGs se definen como archivos Python que describen las tareas y sus dependencias
- Airflow utiliza los conceptos de **Operator**, y **Dependencia**
- Cada tarea es un **Operator** (PythonOperator, BashOperator, etc.)
- Las dependencias se establecen usando los operadores `>>` y `<<`

Ejemplo:
```python
from airflow import DAG
from datetime import datetime

with DAG('mi_dag', start_date=datetime(2024, 1, 1)) as dag:
    tarea_1 >> tarea_2  # tarea_2 depende de tarea_1
```

## Características clave
- **Programación**: Los DAGs pueden ejecutarse en intervalos regulares (diario, semanalmente, etc.)
- **Paralelización**: Las tareas independientes se ejecutan simultáneamente (si tenemos recursos, ¡ojo!)
- **Reintentos**: Configuración automática de reintentos en caso de fallo
- **Monitoreo**: Interfaz web para visualizar el estado de ejecución
- **Backfill**: Posibilidad de ejecutar DAGs para fechas pasadas

# ¿En que se parecen / diferencia los DAGs de Airflow y los de Spark?

## DAGs de Spark

Los DAG en Spark son fundamentalmente diferentes:

- Representan el **plan de ejecución** de transformaciones RDD/DataFrame
- Se construyen automáticamente a partir de código Spark
- Spark los optimiza y ejecuta en un motor distribuido
- Son DAGs de computación distribuida para procesamiento de datos

## Diferencias principales

| Característica | Airflow DAG | Spark DAG |
|----------------|-------------|-----------|
| **Finalidad** | Orquestación de flujos de trabajo | Procesamiento distribuido de datos |
| **Creación** | Manual mediante código Python | Automática a partir de transformaciones |
| **Control** | El usuario define dependencias explicitamente | Spark infiere el grafo de ejecución |
| **Ejecución** | Planificación basada en tiempo | Ejecución en cluster distribuido |
| **Abstracción** | Alto nivel (tareas de negocio) | Bajo nivel (transformaciones de datos) |
| **Escalado** | Horizontal para orquestación | Horizontal para procesamiento |

Es común usar **Airflow para orquestar pipelines** que incluyen **tareas Spark**, combinando así la orquestación de alto nivel de Airflow con el poder de procesamiento distribuido de Spark.
