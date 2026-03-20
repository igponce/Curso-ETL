# Cuándo se ejecutan los dags

En Airflow no marcas un momento concreto, sino un horario.
Puedes utilizar un schedule_interval basado en Cron o algo más sofisticado.


1. **start_date** – el día en que el despertador se estrena (tiene que ser un momento ya pasado).
2. **schedule_interval** – la frecuencia (diaria, semanal, un *cron-expression*…).

Ejemplo: Quiero que un informe se genere todos los días a las 6 a. m.  
```python
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

with DAG(
    dag_id='informe_diario',
    start_date=days_ago(1),   # se «estrenó» ayer
    schedule_interval='0 6 * * *',  # a las 6:00 cada día
) as dag:
    ...
```

La primera vez que se ejecutará será «mañana» al cumplirse 24 h desde start_date. 

Mientras tanto, Airflow lo mantiene «en espera»; no importa que ya hayan pasado varias semanas: cuando decidas publicarlo procesará todas las ejecuciones pendientes sin que tengas que calcular fechas con una libreta.
