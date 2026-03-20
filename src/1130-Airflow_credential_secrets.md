# Credenciales y Secrets

- Conexiones y credenciales en Airflow
  - Separadas del código
  - Se gestionan mediante la interfaz de usuario de Airflow en: Admin → Connections
    - **OJO** Hay que referenciar las credenciales en el código.
    - Esto permite que un admin pueda cambiar credenciales, sin tocar el código, y que el desarrollador de la ETL no tenga que tener conocimiento de las credenciales (usuario, password, host, certificados, etc...)
  - También pueden gestionarse mediante comandos de CLI: `airflow connections add/edit`
  - Se almacenan en la BBDD (Postgres, MySQL o SQLite en desarrollo)
  - Variables y Secrets:
    - En Variables: Admin → Variables (clave-valor en la BBDD)
    - Se puede encriptar el contenido usando FERNET (hay una clave FERNET_KEY que es configurable) 
    - En Secrets Backends: puedes integrar con AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager, Azure KeyVault

```python
from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG('query_postgres',
         start_date=datetime(2023, 1, 1),
         schedule='@daily',
         catchup=False) as dag:

    PostgresOperator(
        task_id='test_query',
        postgres_conn_id='postgres_desarrollo_curso',  # Usa la credencial guardada
        sql='SELECT CURRENT_TIMESTAMP;'
    )
```
