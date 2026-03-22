# Caso práctico

Carga de datos a medida que aparecen en un servidor

Tenemos estos datos (dataset titanic)
https://gist.github.com/igponce/4e02185479bd74989410c74be1d4f4c7

Cada cierto tiempo aparecerán nuevos ficheros CSV con esta información en una carpeta:

```
Passengerid,Age,Fare,Sex,sibsp,zero,zero,zero,zero,zero,zero,zero,Parch,zero,zero,zero,zero,zero,zero,zero,zero,Pclass,zero,zero,Embarked,zero,zero,survived
1,22,7.25,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,2,0,0,0
2,38,71.2833,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1
3,26,7.925,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,2,0,0,1
```

Tenemos que ingestar los datos nuevos cada vez que aparezcan y cargarlos en una base de datos.

Sólo queremos guardar los datos de las 4 primeras columnas.

Entrada: /tmp/incoming
Destino staging: /home/mbit/data/incoming

Tenemos una BBDD Posgres en la que guardaremos los datos.

Hay preparada una tabla `passengers` de staging con todos los campos en modo texto:

```
postgres=# \dS passengers
              Table "public.passengers"
   Column    | Type | Collation | Nullable | Default
-------------+------+-----------+----------+---------
 passengerid | text |           |          |
 age         | text |           |          |
 fare        | text |           |          |
 sex         | text |           |          |
 ```
 
El destino será la tabla `passengers_prod` que ya tiene los tipos de cada campo definidos.

Habrá que pasar la información de una tabla a otra haciendo casting de forma parecida a esta: `SELECT CAST(campo as TIPO_DESTINO) FROM public.passengers `:

```
Table "public.passengers_prod"
Column    |  Type   | Collation | Nullable | Default
-------------+---------+-----------+----------+---------
passengerid | integer |           | not null |
age         | integer |           |          |
fare        | numeric |           |          |
sex         | text    |           |          |
Indexes:
"passenger_prod_pkey" PRIMARY KEY, btree (passengerid)
```

Hay que tener en cuenta que si el campo ya existe (la clave primaria no se puede duplicar), habrá que actualizar el registro de la base de datos.

## Proceso auxiliar

Para simular que se generan ficheros hay un DAG de airflow [99_genera_ficheros.py](/lab/airflow/dags/99_genera_ficheros.py)
en la carpeta [lab](/lab) que copia archivos cada minuto en `/tmp/incoming`

Estrategia de carga:
```mermaid
graph LR
Copiar_Ficheros --> Crear_SQL --> Cargar_en_modo_texto --> Cargar_en_destino 
```
Hay que tener en cuenta que tendremos que borrar los ficheros para no llenar los servidores, pero también tenemos que poder rearrancar procesos por si hay algún error.
