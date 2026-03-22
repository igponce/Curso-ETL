# Introducción

Esta es una guía de estudio para conocer en qué consiste el ETL / ELT.

Los proceoso ETL (Extract, Load, Transform) son fundamentales en los entornos de datos actuales.
Vamos a encontrar estos procesos en múltiples sitios: desde Data Warehouses, Integración de datos, o en entornos analíticos de ciencia de datos.

Lo importante de estos procesos es que sean _precedibles_ y _confiables_.

Nadie se puede permitir un procesar datos sin saber que tiene cargado en el sistema la información correcta.


# Caso práctico

Antes de empezar la parte práctica tienes que instalar Apache Airflow.
Tienes dos opciones: instalarlo con un contenedor (utilizando docker-compose), o instalar Airflow en tu ordenador con pypy o uv y ejecutarlo desde ahí.

Para los ejemplos utilzaremos Airflow3.
Muchas empresas siguen usando Airflow versión 2 porque hay cambios en la interfaz de desarrollo y hay que adaptar los Dags a la versión nueva antes de migrarlos.
Los ejemplos usan la forma "vieja" de definir tareas (aunque tiene más código boilerplate), pero permiten que alguien que tenga que migrar código de v2 a v3 pueda saber lo que hace.
