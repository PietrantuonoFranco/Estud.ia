# Estud.ia
Proyecto RAG para estudios.

## Contenedores
| Contenedor | Puerto | Descripción |
|-------------------|--------|----------------|
| postgres-users | 5432 | Almacena la información de los usuarios en una base de datos PostgreSQL. |
| milvus-etcd | 2379 | Servicio de almacenamiento clave-valor distribuido para la configuración y coordinación de Milvus. |
| milvus-minio | 9000 9001 | Sistema de almacenamiento de objetos S3-compatible para los datos persistentes de Milvus. Puerto 9000 para API, puerto 9001 para consola web. |
| milvus-standalone | 19530 9091 | Base de datos vectorial principal para almacenamiento y búsqueda de embeddings. Puerto 19530 para API, puerto 9091 para métricas. |
| attu | 8001 | Interfaz gráfica de administración para la base de datos vectorial Milvus. |
| chainlit | 8000 | Aplicación de interfaz de usuario para interacción con el sistema RAG. |
| langchain | 80 | API FastAPI para procesamiento de documentos, generación de embeddings y gestión del almacenamiento vectorial. |
| users-api | 5000 | API FastAPI para procesamiento de usuarios y sus hilos. |


#### Repositorio compartido por:
- Franco Pientrantuono
- Ivan Vijandi
