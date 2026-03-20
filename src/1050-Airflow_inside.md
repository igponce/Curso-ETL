# Cómo Funciona Aiflow

Bag of DAGs: al iniciar Airflow carga los DAGs existentes en una carpeta
- Base de datos: almacena información sobre DAGs, ejecuciones, secretos, …
- Scheduler: programa la ejecución de los DAGs
- Checkea cada 5 segundos si debe actuar sobre nueva tarea
- Executor: Motor de ejecución de las tareas (Sequential, Dask, Kubernetes, …)
- Webserver / API: Tareas de gestión y control
