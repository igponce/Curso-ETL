# Ingeniería ETL: Parada, reinicio, y reanudación

Hay que tener en cuenta que durante operación del proceso ETL vamos a tener que lanzar, parar, dar marcha atrás, y reanudar procesos.

## ¿Esto cómo se para?

¿Quién no ha lanzado nunca un proceso que no debía?
¿O lo ha lanzado apuntando al entorno equivocado?
¿O lo ha lanzado con los parámetros incorrectos?

Si te equivocas haciendo un `SELECT` en la base de datos puedes cancelarlo matando el proceso.

Postgres: como averiguar el PID de un proceso en ejecución
```sql
SELECT pid, query FROM pg_stat_activity WHERE query LIKE '%SELECT%';
```

Postgres: como cancelar un procesoparar un proceso
```sql
SELECT pg_cancel_backend(pid);
```

En un proceso de ETL, el orquestador se encarga por tí de terminar estos procesos.

## ¿Y cómo doy marcha atrás?

Dar marcha atrás es mucho más complejo que sólo parar un proceso.

Los procesos de carga suelen tener muchas dependencias, y dar marcha atrás suele implicar borrar datos ya cargados.
En este caso lo que hay que hacer es borrar el dato hasta un punto de control que puede ser, por ejemplo, un día/hora, o último fichero cargado.

## ¿Y cómo reanudo?

Reanudar un proceso de carga es más fácil que dar marcha atrás, pero puede tener complicaciones porque haya datos ya cargados y es posible que no se puedan cargar de nuevo (o no se puedan sobreescribir).

En muchas ocasiones es más sencillo crear una transacción, y si no se dan unas condiciones de calidad, hacer un rollback.
Por ejemplo, esto es lo que hace la heramienta `dbt`: si no pasan los tests, hace un rollback.
