# Ingeniería ETL: Control de tiempos

Es tan importante saber QUÉ se ejecuta tanto como decidir CUÁNDO se ejecuta.

Los sistemas que son el origen de nuestros datos no siempre va a tener la misma carga durante todo el día.
Puede haber variaciones no sólo dependiendo de la hora del día; sino también del día de la semana y si es un día festivo.

Lo más común es que el dueño del transaccional nos permita hacer la operación de extracción o de carga (en un ETL inverso) duranta una *ventana temporal*

## Caso práctico

Tenemos un data warehouse que recibe datos de transaccionales de una empresa.
Los sisttemas que tenemos son:
- SAP para contabilidad (facturas, albaranes)
- Salesforce para CRM (clientes, ventas)
- Manhattan para gestión del almacen (inventario, almacenamiento, logística, planning de stock)
- Software a medida para cajas registradoras
- Azure Entra como origen de usuarios

Con estas ventanas de tiempo en las que podemos acceder a los sistemas:

¿Podemos identificar qué % de un pedido que llega a almacén está vendido de antemano?

```mermaid

gantt
    dateFormat  HH:mm
    axisFormat %H:%M
    SAP          : 03:00, 90m
    Almacen      : 00:00, 6h
    Salesforce         : 06:00, 180m
    Azure_SSO_Users   : 03:00, 05:00
    Cajas_Registradoras  : 00:00, 4h
 ```
