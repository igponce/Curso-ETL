# Estructura interna de Airflow

Despés de ejecutar `$ airflow db init` (o `airflow standalone`) tenemos una estructura de directorios como esta:

```text
$AIRFLOW_HOME/
├── airflow.cfg               # Configuración global
├── airflow.db                  # Metadatos SQLite (por defecto)
├── webserver_config.py         # Parámetros adicionales de la UI
├── logs/                       # Logs por tarea
│   └── dag_id/
│       └── task_id/
├── plugins/                    # Controles extra, Hooks, Operators… que se cargan automáticamente
├── config/                     # Archivos de entorno (Variables, Secrets-Backend, etc.)
├── scripts/                    # Helpers operativos para admins
└── dags/                       # ⬅️  ******* TU CÓDIGO VIVE AQUÍ *****
    ├── dag_1.py
    ├── …
    └── helpers/
```

## ¿Qué es el directorio `dags/`?

### Repositorio de código de DAGS.   
   - El scheduler y el webserver escanean en caliente todos los archivos Python presentes en `dags` cada `dag_dir_list_interval` (por defecto 5 min).  
   - Cada archivo que defina al menos una instancia de `airflow.DAG` aparecerá automáticamente en la UI y quedará programada para ejecución.
   - Es muy normal que este directorio esté montado, por ejemplo en un bucket, y que un proceso CI/CD vuelque aquí los cambios.

### Sistema de carga dinámica  
   - Airflow no necesita reinicio cada vez que añadas, modifiques o borres un DAG.

   - El proceso de *parsing* compila el archivo en busca de la variable global `dag` (o `dags`) y genera un objeto interno que será almacenado en la base de datos (`dag_code`, `dag_run`, etc.).

### Aislamiento del resto de componentes de Airflow  
   - Separar los scripts de transformación (`dags/`) de los logs, plugins o configuraciones evita conflictos de importación.

### CI/CD (Integración continua/despliegue continúo)  
   - Al mantener únicamente esta carpeta bajo control de versiones (Git) puedes desencadenar *despliegues automatizados* mediante `rsync`, K8s `git-sync`, `git pull`, etc. sin tocar el runtime de Airflow.
