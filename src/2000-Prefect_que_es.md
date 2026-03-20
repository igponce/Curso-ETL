# ¿ Qué es Prefect?

Evolución de Airflow desarrollada por Creado por Jeremiah Lowin (PMC de Airflow) en 2018.

### Modelo de ejecución híbrido

Prefect utiliza un **modelo híbrido** con estos dos compnentes:

| Componente | Responsabilidad |
|---|---|
| **Prefect Core** | Código propio / agentes / (y datos) ejecutado en nuestra infraestructura |
| **Prefect Cloud** | Orquestación y API como un servicio |

Ambos componentes se comunican de forma segura: el código y los datos nunca salen de tu infraestructura, mientras que la orquestación y la API se gestionan en la nube.

---

### Prefect Cloud — Planes

| Plan | Descripción | Características principales |
|---|---|---|
| **Free** | Para proyectos personales | Funcionalidades esenciales, sin tarjeta de crédito, límite de 5.000 runs/día, 2 usuarios |
| **Pro** | Para startups y equipos pequeños | Hasta 20 usuarios, SSO (SAML/OIDC), retención extendida de datos y logs, soporte 9×5 |
| **Enterprise** | Para requisitos más estrictos | Permisos granulares y RBAC, Directory Sync (SCIM), IP allowlisting y PrivateLink, soporte 24×7 |

> Acceso: [https://app.prefect.cloud/](https://app.prefect.cloud/)

## Conceptos

- **Workers & pools**: procesos encargados de ejecutar flujos almacenados en una
cola (worker pool). Pueden ser workers activos (agentes) o pasivos (i.e. AWS
ECS)
- **TaskRunner**: Motor de ejecución de las tareas (DaskTaskRunner,
ConcurrentTaskRunner, ...)
- **Infraestructura**: Infraestructura donde ejecutar los flujos (i.e.: Process, Docker,
Kubernetes)
- **Storage**: permite serializar, almacenar y recuperar los flujos

(Concepto similar a CI/CD tipo Gitlab, AzureDevops, pero con nuestros datos y procesos *en nuestra casa*)

Nota: Alguna de las características de prefect se han portado a Airflow, como el uso de decoradores para dags, tareas, etc...
