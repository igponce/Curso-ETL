# Ingeniería ETL: Observabilidad

Cuando tenemos un proceso automático siempre tenemos la mismad preguntas:

- ¿Qué ha ocurrido?
  - ¿Ha ido bien?
  - ¿Ha ido mal?
    - ¿Dónde ha fallado?
    - ¿Qué ha ocurrido?
    - ¿Cómo se puede solucionar?
    - ¿Hay que volver a ejecutar todo desde el principio?

El orquestador de la ETL nos puede dar alguna pista sobre esto.
Sin embargo, tenemos que tener siempre un control de la observabilidad.

(Nota: Observabilidad no se refiere a tener un call log, y un flamegraph en Elastic o en Datadog; sino a ser capaces de saber el estado del proceso que se lanza automáticamente)

## Controles sencillos

Algunos controles sencillos que podemos implementar nosotros son:

### Registro en una base de datos

Registramos en una base de datos metadata sobre el proceso ETL.
Por ejemplo: 

| campo | valor |
| ---- | ---- |
| proceso | Nombre del proceso ETL |
| fase | Fase actual del proceso ETL |
| ts | Timestamp de la ejecución |
| entrada | Número de registros de entrada |
| salida | Número de registros de salida |
| errores | Número de errores |

Con un esquema tan sencillo podemos identificar qué proceso y fase no se ha ejecutado símplemente
con un `SELECT ts, proceso, fase FROM log_etl where entrada = 0`.

Podemos poner estas consultas en un dashboard para tener una visión general del estado de los procesos ETL y saber qué ha pasado sin necesidad de hacer consultas a mano.

### Logs

Un simple mensaje de log, agregado en un recolector central es una herramienta muy potente para saber qué ocurre.
Los clouders te pueden enviar los logs que emiten tus máquinas a sus logs centralizados, por lo que es muy cómodo de usar.

Cuando usamos logs hay que tener muy en cuenta cuánto tiempo los mantenemos para hacer consultas.

Hoy en día se pueden madar logs semi-estructurados con un `payload` JSON que podemos usar para filtrar (google, elastic, etc).
