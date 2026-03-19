# ETL vs. Reverse ETL

Ahora que sabemos qué es una ETL ¿qué es una Reverse ETL?

## ¿Qué es Reverse ETL?

- **Extract:** Sacar datos desde un almacén central (DW, Datalake, Snowflake, BigQuery…).  
- **Transform (opcional):** Ajustar el formato o agregar lógica de negocio antes de la entrega.  
- **Load:** Insertar o sincronizar esos datos en sistemas operacionales (CRM, SaaS, herramientas de marketing, etc.).

** La diferencia está en que YA tenemos un lugar central desde el que extraemos información **

¿Qué información? Por ejemplo

- Maestro de clientes (todos los clientes se llamarán igual en _todas_ nuestras aplicaciones ).
- Maestro de productos (a veces recibimos productos de distintos suministradores, aunque el fabricante sea el mismo)

## Reverse ETL NO ES un DATA MESH ##

Puede ser tentador pensar en un data mesh como una Reverse ETL.

NO es así.

El data mesh te oculta "lo que hay debajo".

Vas a tener unas interfaces cerradas para acceder al dato y el data mesh se encarga de que el dato sea consistente.

Una Reverse ETL no es una data mesh. Es el proceso que te permite coordinar la información de distintos sistemas para que luego puedas tener un dato coherente a través de los sistemas (y lo puedas juntar, o borrar de forma coherente). 

## Comparación ETL ↔ Reverse ETL
| Característica | ETL | Reverse ETL |
|----------------|-----|--------------|
| **Dirección del flujo** | Fuente → Destino (central) | Destino (central) → Fuente (operacional) |
| **Objetivo principal** | Consolidación y análisis histórico | Activación operativa y personalización en tiempo real |
| **Arquitectura típica** | Data‑warehouse / Data‑lake | Data‑warehouse → APIs, webhooks, integraciones SaaS |
| **Frecuencia** | Batch (horaria, diaria, semanal) | Near‑real‑time o batch ligero |

## Casos de uso de Reverse ETL

- **Sincronización de audiencias** entre el DW y plataformas de publicidad (Google Ads, Meta).  
- **Enriquecimiento de CRM** con métricas de comportamiento (p. ej., scoring de leads).  
- **Personalización en tiempo real** en apps móviles o webs usando datos de comportamiento.  
- **Automatización de flujos** en herramientas de marketing (Mailchimp, HubSpot) con datos actualizados.

## ¿ Donde esta "LA VERDAD" ?

- La verdad está en los sistemas -> ETL
- La verdad hay que enviarla a los sistemas -> Reverse ETL

En el mundo real(tm) lo normal es que la información "aparezca" en un sistema, tomes esa información como "la verdad", y la propagues al resto de sistemas.
Para eso, te quedas (o construyes) un "golden record".

## Ventajas y retos ETL / Reverse ETL
### ETL
- **Ventajas:** Calidad y consistencia de datos, historial completo, soporte para grandes volúmenes.  
- **Retos:** Latencia (batch), complejidad de transformación, coste de infraestructura.

### Reverse ETL
- **Ventajas:** Datos “activados” en tiempo real, mejora de la experiencia del cliente, reducción de silos.  
- **Retos:** Necesidad de mantener la sincronización, gestión de cambios de esquema, seguridad en la exposición de datos.
