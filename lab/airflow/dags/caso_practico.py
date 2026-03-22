from datetime import datetime, timedelta

from airflow.operators.python import PythonOperator

# Si buscas en la documentación aparece esto pero FALLA el import:
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# Hay que usar este en su lugar (lo usan los tests de Airflow).
# ¿El motivo? Airflow3 está cambiando las interfaces -> cuidado con el vibe coding.
# Algunos LLMs no han memorizado  esto todavía y te darán problemas.
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.standard.operators.bash import BashOperator

from airflow import DAG

# ---------------------------  CONFIGURATION  --------------------------- #
# Modify these values to fit your project.
DAG_ID = "0002_Practica_ingesta"
DESCRIPTION = "DAG that runs every 5 minutes or can be triggered manually."
TAGS = ["boilerplate", "development", "inigo"]
MAX_RUNTIME_MINUTES = 10  # fail after N minutes if task still running
RETRY_ATTEMPTS = 0  # fail fast during dev, increase in prod
RETRY_DELAY_MINUTES = 2
# -------------------------------------------------------------------------- #


# ---------------------------  PYTHON CALLABLES  ---------------------------- #
def lee_fichero_csv(**context):
    """
    Leemos el CSV y nos quedamos solo con los 4 primeros campos
    """
    dag_run = context["dag_run"]
    print(f"Hello from DAG run {dag_run}")
    # TODO: Replace with real work.


def procesa_fichero_a_lo_loco():
    """
    Creamos dos ficheros:
      - splitted.sql -> Contiene los cuatro primeros campos del CSV.
      - filelist     -> Lista de archivos que hemos procesado

      **IMPORTANTE** Esta función crea un fichero SQL dentro
         del directorio DAGs de Airflow !!!!

         La inserción en la BBDD necesita un SQL, o un fichero.sql

        ** ESTO NO ES UNA BUENA PRACTICA Y NO SE RECOMIENDA **
        Ese directorio será el resultado de un proceso CI/CD
        ¿Donde podemos poner el fichero? Si lo volcamos a un directorio
        y el operador que ejecuta el SQL se lanza en una máquina distinta
        la ETL fallará....

        Para comunicar
    """
    import glob

    # Vamos a procesar

    with open("/home/mbit/data/out/inigo/filelist", "w") as filelist:
        with open("/home/mbit/airflow/dags/staging.sql", "w") as outfile:
            for ff in glob.glob("/home/mbit/incoming/inigo/*.csv"):
                with open(ff, "r") as fp:
                    for line in fp.readlines()[1:]:
                        campos = line.split(",")
                        output = ",".join(
                            [f"'{x}'" for x in campos[0:4]]
                        )  # Hay que adaptar el dato y poner comilla simple
                        insert_statement = f"INSERT INTO passengers VALUES ({output});"
                        outfile.write(f"{insert_statement}\n")
                filelist.write(f"{ff}\n")


# Callables - lo utilizaremos más abajo con un Python Operator


def procesa_ficheros_XCOM(**context):
    """
       Vamos a comunicar los procesos de ETL usando XCOM, que es
       un mecanismo de Airflow para comunicar procesos de ETL
       sin que tengan que compartir recursos.

       Tiene algunos problemas:
         1. El contenido que pasamos por XCOM se guarda en la BBDD.
            Hay que purgarlo periódicamente -> MANTENIMIENTO
         2. Los contenidos no están cifrados. Una copia de seguridad
            de la base de datos puede contener info sensible -> LEGAL.

        Para recuperar estos contenidos utilizamos plantillas JINJA
        https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html

        La idea es:
           1. Procesar los datos.
           2. Enviar a XCOM el contenido.
           3. Ejecutar el operador cargando el contenido desde una plantilla.

    Creamos dos XCOM:
      - splitted.sql -> Contiene los cuatro primeros campos del CSV.
      - filelist     -> Lista de archivos que hemos procesado
    """
    import glob

    FILELIST_PATH = "/home/mbit/data/out/inigo/filelist"
    SQLFILE_PATH = "/home/mbit/airflow/dags/staging.sql"
    CSV_GLOB = "/home/mbit/incoming/inigo/*.csv"

    # Vamos a procesar los ficheros entrantes

    with open(FILELIST_PATH, "w") as filelist:
        with open(SQLFILE_PATH, "w") as outfile:
            for ff in glob.glob(CSV_GLOB):
                with open(ff, "r") as fp:
                    for line in fp.readlines()[1:]:
                        campos = line.split(",")
                        output = ",".join(
                            [f"'{x}'" for x in campos[0:4]]
                        )  # Hay que adaptar el dato y poner comilla simple
                        insert_statement = f"INSERT INTO passengers VALUES ({output});"
                        outfile.write(f"{insert_statement}\n")
                filelist.write(f"{ff}\n")

    # Hasta aquí todo exactamente igual. Vamos a mandar a XCOM los contenidos.
    # Vamos a leer los ficheros que hemos generado y los mandamos a XCOM.
    # Podríamos haber creado todo en memoria y enviarlo después.

    # Para hacer un push de datos a XCOM necesitamos la instancia de la tarea
    # En este proceso usamos el argumento **context que contiene metadata
    # y objetos de Airflow necesarios para que este callable se ejecute.

    with open(FILELIST_PATH, "r") as fp:
        context["ti"].xcom_push(key="filelist", value=fp.read())

    with open(SQLFILE_PATH, "r") as fp:
        context["ti"].xcom_push(key="sql", value=fp.read())


# --------------------------------------------------------------------------- #


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
    DAG_ID,
    description=DESCRIPTION,
    tags=TAGS,
    default_args=default_args,
    # Automatic execution rules
    schedule="*/10 * * * *",  # cada 10 minutes
    catchup=False,  # prevent backfilling on first deploy
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=MAX_RUNTIME_MINUTES),
)

with dag:
    copia_ficheros_entrantes = BashOperator(
        # como queremos llamar a este 'step'
        # que queremos ejecutar
        task_id="copia_incoming",
        bash_command="cp /tmp/incoming/*csv /home/mbit/incoming/inigo",
    )

    borrar_ficheros_entrantes = BashOperator(
        task_id="borra_ficheros_entrada", bash_command="rm /tmp/incoming/*csv"
    )

    borrar_ficheros_staging = BashOperator(
        task_id="borra_ficheros_staging",
        bash_command="rm $(cat /home/mbit/data/out/inigo/filelist)",
    )

    """
    leer_ficheros = PythonOperator(
        task_id = "lee_csv",
        python_callable = procesa_fichero_a_lo_loco,
    )
    """

    leer_ficheros = PythonOperator(
        task_id="lee_csv",
        python_callable=procesa_ficheros_XCOM,
    )

    insert_into_staging = SQLExecuteQueryOperator(
        task_id="insert_into_staging",
        conn_id="staging",  # Definido en la config de Airflow.
        # Para ver qué hacer la BBDD en los logs
        hook_params={"enable_log_db_messages": True},
        # Este es el caso de la mala paráctica sin XCOM
        # sql = "staging.sql" # SQL que hemos generado en el Python Operator
        # Hacemos pull en XCOM la clave del sql que hemos hecho push antes.
        # Necesitamos el id de la tarea que ha generado el contenido a compartir.
        # OJO! Sigue estando disponible!!!
        sql="{{ ti.xcom_pull(key='sql', task_ids='lee_csv') }}",
        # IMPORTANTE -> Esto no es una buena práctica.
        # Los DAGs suelen estar en un bucket o un disco compartido.
        # No se tiene que poder escribir nada allí: es como modificar
        # tu propio código, igual que haría un virus.
        # Para comunicar distintos operadores Airflow tiene un
        # mecanismo llamado XCOM que veremos después.
    )

    insert_into_prod = SQLExecuteQueryOperator(
        task_id="staging_to_prod",
        conn_id="prod",
        # Este SQL es muy largo -> podriamos tener on un fichero
        sql="""INSERT INTO passengers_prod AS tgt
                SELECT DISTINCT ON (passengerid)
                    passengerid::int,
                    FLOOR(age::float)::int,
                    fare::float,
                    sex
                FROM   passengers
                ORDER  BY passengerid, age NULLS LAST   -- elije el que tenga age no-nulo si hay varios
                ON CONFLICT (passengerid)
                DO UPDATE
                SET age  = EXCLUDED.age,
                    fare = EXCLUDED.fare,
                    sex  = EXCLUDED.sex;
               """,
    )

    # Borrar staging

    truncate_staging = SQLExecuteQueryOperator(
        task_id="truncate_staging", conn_id="staging", sql="TRUNCATE passengers"
    )

    # ---------------------------  TASK FLOW  ------------------------- #

    copia_ficheros_entrantes >> leer_ficheros
    leer_ficheros >> insert_into_staging
    leer_ficheros >> borrar_ficheros_entrantes
    insert_into_staging >> borrar_ficheros_staging
    insert_into_staging >> insert_into_prod
    insert_into_prod >> truncate_staging

# ----------------------------------------------------------------------- #
