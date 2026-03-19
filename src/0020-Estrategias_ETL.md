# Estrategias ETL

Antes de empezar a codificar una ETL y orquestarla tenemos que pensar (muy bien) qué estrategia vamos a seguir.

Hay que tener en cuenta que la información va a pasar por una infraestructura que estará compartida entre varios servicios y el movimiento de datos puede poner en peligro la integridad.

[Poll: ¿Qué puede ir mal en una ETL?]

Ejemplos de cosas que pueden ir mal:

- Saturación en una línea
- Saturación de un elemento compartido (firewall)
- Locking en la base de datos
- Cuotas de API sobrepasadas
- Cloud Outage

# Cómo minimizar problemas: Estrategia

Por regla general ***cuanto más tardes en hacer la extracción de datos, más posibilidades hay de que algo vaya mal*** PERO hay excepciones.

# Minimizar problemas: Identifica Riesgos

- Asegurate de que conoces las dependencias de los datos y sistemas que va a atravesar al ETL.
- Cuando algo ocurra, no puedes respoder "no lo sé".

## Averigua por dónde van a pasar tus datos?

- Antes de mover datos, tienes que saber por dónde va a ir el dato.
- ¿Hay algún elemento compartido?
- ¿Estás saturando una línea al mover los datos?


Para evitar que una ejecución de ETL se haga fuera de hora tenemos orquestadores de ETL.


## Modelo en capas
