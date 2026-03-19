import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Esto es lo que vamos a ejecutar.
# Simulamos algo que tarda 5 segundos en ejecutarse
# Don't panic: enseguida veremos algo que se parece más al mundo real.


def sleep_task(**context):
    """Simulamos una tarea que tarda 5 seconds"""
    print("Starting sleep task...")
    time.sleep(5)
    print("Sleep task completed!")


default_args = {
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Creamos el dag.
dag = DAG(
    "010_Sleep_DAG",
    default_args=default_args,
    description="Ejemplo de dag que simula un proceso que tarda un poco en ejecutarse",
    schedule_interval=timedelta(days=1),
    catchup=False,
)

sleep_operator = PythonOperator(
    task_id="sleep_task",
    python_callable=sleep_task,
    dag=dag,  # Hay que enlazarlo con el DAG.
)
