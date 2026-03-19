# ¿Qué es Apache Airflow?

Apache Airflow es una plataforma **open-source** desarrollada originalmente por Airbnb en 2014 para programar, supervisar y gestionar flujos de trabajo (workflows) de forma programática.

En 2016, se convirtió en un proyecto de la **Apache Software Foundation**.

## Todo se basa en código

**IMPORTANTE** A diferencia de otras herramientas, que te permiten trabajar de distintas maneras, Apache Airflow es **opinionated**: es decir, te obliga a trabajar de una manera determinada.

Airflow permite definir, ejecutar y monitorear flujos de trabajo como **código**. 

Esto significa que puedes describir tus procesos ETL (Extract, Transform, Load) usando lenguajes de programación como Python, lo que facilita el versionado, testing y colaboración.

Esto quiere decir que una persona con acceso a la interfaz de usuario *no puede* modificar los flujos de trabajo.


## ¿Por qué es Importante?

### 1. **Infraestructura como Código (Infrastructure as Code)**
- Todos los flujos de trabajo se definen en archivos de código
- Facilita el control de versiones con Git
- Permite revisión de código y colaboración entre equipos
- Permite trazar quién ha cambiado algo, cuándo, y (si estás trabajando de una manera determinada), también el porqué.

### 2. **Flexibilidad**
- Define flujos de trabajo complejos con dependencias específicas
- Ejecuta tareas en orden o en paralelo
- Maneja condicionales
- En caso de que un job falle podemos volver a ejecutar los nodos que han fallado.

### 3. **Escalabilidad**
- Distribuye tareas entre múltiples workers
- Gestiona grandes volúmenes de procesamiento
- Integración con sistemas como Kubernetes
  - Recordad: KubernetesOperator

### 4. **Monitorización Avanzada**
- Interfaz web intuitiva para visualizar flujos de trabajo
- Seguimiento en tiempo real de tareas
- Logs centralizados y notificaciones de errores

## Componentes Principales

### DAG (Directed Acyclic Graph)
El corazón de Airflow es el **DAG**, que representa:
- **Directed**: Las tareas tienen una dirección específica
- **Acyclic**: No hay ciclos (no puedes volver a una tarea ya ejecutada)
- **Graph**: Conjunto de tareas conectadas mediante dependencias

### Operadores (Operators)
Define qué se ejecuta:
- `PythonOperator`: Ejecuta funciones Python
- `BashOperator`: Ejecuta comandos bash
- `PostgreSQLOperator`: Ejecuta queries SQL
- `HTTPOperator`: Realiza peticiones HTTP

### Sensores (Sensors)
Esperan por eventos específicos:
- Esperar por un archivo
- Esperar por una API
- Esperar por una database
- Esperar por un email
- Esperar que termine de ejecutarse un operador

## Casos de Uso en ETL

### 1. **Procesamiento de Datos**
```python
# Extraer datos de APIs
extraer = PythonOperator(task_id='extraer_datos', python_callable=extraer_de_api)

# Transformar datos
transformar = PythonOperator(task_id='transformar_datos', python_callable=limpiar_y_normalizar)

# Cargar a data warehouse
cargar = PythonOperator(task_id='cargar_dw', python_callable=cargar_a_redshift)
```

### 2. **Workflows de Reporting**
- Generación de reportes diarios
- Envío de emails con métricas
- Actualización de dashboards

### 3. **Migración de Datos**
- Sincronización entre bases de datos
- Copia de seguridad de datos
- Consolidación de fuentes

## Arquitectura Airflow

```
┌─────────────────┐
│   Scheduler     │
│  (Planificador)  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Metastore     │
│  (PostgreSQL)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Celery Workers │
│  (Ejecutores)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Web Server     │
│  (UI Interface)  │
└─────────────────┘
```

## Ventajas vs Herramientas Tradicionales

| Característica | Airflow | Cron | Herramientas GUI |
|----------------|---------|------|------------------|
| **Dependencias** | ✓ Soporte complejo | ✗ Limitado | ✓ Parcial |
| **Monitorización** | ✓ Interfaz web | ✗ Logs básicos | ✓ Variable |
| **Escalabilidad** | ✓ Alta | ✗ Manual | ✓ Media |
| **Versionado** | ✓ Git-friendly | ✗ Archivos conf | ✗ Propio sistema |
| **Testing** | ✓ Framework integrado | ✗ Manual | ✗ Limitado |

## Instalación Básica

```bash
# Instalar Airflow
pip install apache-airflow

# Inicializar base de datos
airflow db init

# Crear usuario administrador
airflow users create --username admin --password admin --firstname tu_nombre --lastname tu_apellido --role Admin --email tu@email.com

# Iniciar servicios
airflow webserver --port 8080  # Terminal 1
airflow scheduler              # Terminal 2
```

## Conclusión

Apache Airflow es la **herramienta estándar** para gestionar flujos de trabajo de datos modernos. Su enfoque de "código primero" permite a los ingenieros de datos crear, mantener y escalar pipelines ETL de manera robusta y reproducible.

En el mundo Big Data y análisis avanzado, Airflow se ha convertido en un componente fundamental para orquestar procesos de transformación de datos a escala empresarial.