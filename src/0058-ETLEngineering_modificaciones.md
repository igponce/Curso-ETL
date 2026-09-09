# Ingeniería ETL: Modificaciones y parametrización

Durante la operación tenemos que poder modificar fácilmente la ETL.
No sólo para corregir errores; sino para adaptarnos a ciertos parámetros de los datos de entrada.
Por ejemplo, si se añaden columnas o filas; o también si queremos ejecutar los scripts de ETL con unos parámetros de funcionamiento distintos.

Imagínate que tenemos un proceso que carga en el datawarehouse los datos de ventas del día anterior.
Si lo lanzamos tarde (a las 00:01 en vez de a las 23:30) podemos encontrarnos con que hay datos que no se han cargado.

Tenemos que ser capaces de modificar la ETL para que se ejecute con otros parámetros.

## Parametros de ejecución

Hay muchas maneras de parametrizar la ejecución de un proceso.
En las ETL las más comunes son:

- Variables de entorno: gestionadas por el orquestador. Se puede usar para pruebas durante el desarrollo.
- Registros en base de datos: gestionada por el desarrollador. Es más costoso de usar para pruebas (el CI/CD tiene que tener acceso a una base de datos con un schema concreto).
- Ficheros de configuración: gestionados por el desarrollador. Es más fácil de usar para pruebas (el CI/CD puede tener acceso a un fichero de configuración en el repositori
- Secrets: gestionados por el desarrollador y orquestador. Se usa para datos como contraseñas o claves de API que no deben ser públicos.

## Control de versiones y testing

Al desarrollar ETLs estamos creando código que mostrará datos a partir los de los que la empresa
tomará decisiones (si están en un datamart), o se usarán para la operativa de la empresa (reverse ETL).

Lo importante es que el código que compone la ETL sea trazable desde una petición de usuario hasta la ejecución en producción.

![Trazabilidad](images/trazabilidad_versiones.png)

Con un esquema como el de arriba tenemos esta trazabilidad.
Los cambios de código no se hacen gratuitamente, y queda enlazado en el control de versiones qué cambios hay y porqué usando los documentos de requisitos.

## Testing

Este tema es muy extenso, pero hay que tener en cuenta que el testing sirve para estar seguros de que el código hace lo que se espera, incluso aunque haya errores.

La forma más elegante de gestionar estos test es la de `dbt` que crea una batería de tests orientados a calidad de datos durante la ejecución de la ETL, pero que se pueden usar para asegurarnos de que tenemos una salida correcta a partir de unas entradas.
