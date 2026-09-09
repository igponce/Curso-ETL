# Ingeniería ETL: Control de rendimiento

Los procesos que ejecutamos no están en un entorno con recursos infinitos.

Necesitamos memoria, CPU, almacenamiento, y tiempo para ejecutarlos.

Del ejemplo del crontab tenemos claro que el tiempo de ejecución es importante.
Si nos saltamos una ventana de intervención, podemos afectar a la ejecución del transaccional.

Tambien necesitamos controlar cuánta memoria usamos.
¿Nuestra ETL se ejecuta en un container? Si sobrepasamos la memoria asignada, el contenedor se reinicia.

¿Cuánta CPU necesitamos? A mayor necesidad de CPU, mayor coste.

## Qué nos limita

Si nuestra ETL es `cpu-bound` podemos hacer que la ejecución sea más rápida distribuyendo la carga en varias máquinas que trabajan en paralelo.

Si el job depende de la memoria (`memory-bound`) tendremos que usar equipos con más memoria y menos CPU, o estaremos pagando por recursos de CPU que no vamos a necesitar.

Si tenemos mucha E/S a disco (`io-bound`), tendremos que provisionar IOPs suficientes para evitar que nuestra ETL tarde más tiempo del que debe.
