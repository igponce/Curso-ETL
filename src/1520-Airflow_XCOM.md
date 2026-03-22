# XCOM

## ¿Qué es XCOM en Airflow?

XCOM (abreviatura de "Extended Communications") es el mecanismo que Airflow utiliza para el intercambio de mensajes (metadatos) entre sus tareas. Es decir, permite que una tarea «empuje» valores para que otras tareas posteriores los «tomen» y sigan con la lógica del flujo de trabajo.

Internamente Airflow serializa el valor (pickle o json si se activa la opción) en la base de datos metadatos y lo asocia al `dag_id`, `task_id` y al `execution_date / logical_date` correspondiente.

Por defecto cada clave/valor se almacena sólo si su tamaño no supera los 48 KB; puedes cambiarlo con la variable de entorno `AIRFLOW__CORE__XCOM_MAX_SIZE` o en el fichero airflow.cfg

El uso corriente consiste en que una tarea produce un valor que va a necesitar una tarea posterior-

Por ejemplo, una tarea puede volcar datos a un bucket s3 generando un nombre de fichero identificado por un uuid ( por ejemplo: `s3://bucket/<<uuid>>.csv` ), y una tarea posterior necesita ese dato como entrada.

La primera tarea haría un "push" de esta información vía XCOM utilizando una clave, y la segunda tarea haría un "pull" de esta información utilizando la clave, y el id de la tarea que lo ha generado (la clave primaria en XCom es el id de tarea y la clave).

## Uso de XCom en plantillas Jinja

Las plantillas de Airflow se procesan con [Jinja](https://jinja.palletsprojects.com/en/stable/templates/).

Puedes inyectarlo en: `bash_command`, `arguments`, `sql`, `config`, etc cualquier parámetro marcado con `template_fields` (o `template_ext`) del operador.

Ejemplos:

### BashOperator

Inyectar un fichero generado por otra tarea:

```python
t1 = BashOperator(
    task_id="build_command",
    bash_command="cat {{ ti.xcom_pull(task_ids='get_file_path') }}"
)
```

### SQLExecuteQueryOperator

Pasar un ID calculado al WHERE:

```python
get_max = SQLExecuteQueryOperator(
    task_id="get_max_id",
    python_callable=lambda: 42
)

use_max = SQLExecuteQueryOperator(
    task_id="use_id",
    sql="""
        UPDATE produccion
           SET estado = 'FINALIZADO'
         WHERE id = {{ ti.xcom_pull(task_ids='get_max_id') }};
    """
)
```


### KubernetesPodOperator ‑ inyectar como variable de entorno:

```python
compute_shard = PythonOperator(..., python_callable=lambda: "shard-07")

k8s = KubernetesPodOperator(
    task_id="run_pod",
    image="myapp:1.2",
    env_vars={"SHARD": "{{ ti.xcom_pull(task_ids='compute_shard') }}"}
)
```

El operador tiene que estar dentro del mismo DAG run (misma `execution_date / logical_date`).

Si tu DAG va a generar varias ejecuciones simultáneas, no hay problema: cada ejecución tiene su propio espacio de XCom.
