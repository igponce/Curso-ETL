# Ingeniería ETL: Ejecución de ETL

Si sólo tenemos un único proceso ETL, nos basta con un cronjob para ejecutarlo.

```crontab
# Ejecutar ETL todos los lunes a las 8:00 AM
#Minuto Hora DiaMes Mes Año DiaSemana /path/to/etl/script.sh
0 8 * * 1 /path/to/etl/script.sh
```

También podemos usar un Job de Kubernetes si lo tenemos containerizado

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: etl-create-
spec:
  template:
    spec:
      containers:
      - name: job-create-daily-fact-salest-table
        image: custom-postgresql:20260830
        command: ["psql", "-h", "dbserver", "-f", "/etl/etl-create-daily-fact-sales.sql"]
      restartPolicy: Never
  backoffLimit: 4
```

Sin embargo, para trabajos más complejos en los que el resultado de un proceso es la entrada (o parte de la entrada) de otro proceso, tenemos que usar un orquestador como Apache Airflow, Dagster, Prefect..

Sea cual sea el lugar donde se ejecuta la ETL, debemos tenerlo identificado y documentado para poder solicitar accesos, monitorizarlo, y realizar cualquier ajuste.
