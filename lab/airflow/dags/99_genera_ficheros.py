"""
99_genera_ficheros.py

Genera ficheros cada minuto para simular que nos 
envían datos desde otro sistema
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator


# ---------------------------  CONFIGURATION  --------------------------- #
# Modify these values to fit your project.
DESCRIPTION = "DAG that runs every 5 minutes or can be triggered manually."
TAGS = ["practica"]
MAX_RUNTIME_MINUTES = 10  # fail after N minutes if task still running
RETRY_ATTEMPTS = 2  # fail fast during dev, increase in prod
RETRY_DELAY_MINUTES = 2
# -------------------------------------------------------------------------- #


# ---------------------------  DEFAULT ARGUMENTS  ----------------------------- #
default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "start_date": datetime.utcnow() - timedelta(days=1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": RETRY_ATTEMPTS,
    "retry_delay": timedelta(minutes=RETRY_DELAY_MINUTES),
    "max_active_runs": 1,  # only run one DAG run at a time
}
# -------------------------------------------------------------------------- #


# ---------------------------  DAG DEFINITION  ----------------------------- #
dag = DAG(
    "99_Genera_ficheros", # DAG ID
    description=DESCRIPTION,
    tags=TAGS,
    default_args=default_args,
    # Automatic execution rules
    schedule="*/1 * * * *",  # every 5 minutes
    catchup=False,  # prevent backfilling on first deploy
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=MAX_RUNTIME_MINUTES),
)

with dag:

    crea_fichero = BashOperator(
        # como queremos llamar a este 'step'
        # que queremos ejecutar
        task_id = "crea_fichero",
        bash_command = 'cp /tmp/generate/file.csv /tmp/incoming/file_$(date +%Y%m%d%H%M%S).csv'
    )

    crea_fichero
