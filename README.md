# 📚 Estud.ia - Plataforma RAG para Estudios

Una plataforma moderna basada en **Retrieval Augmented Generation (RAG)** diseñada para optimizar la experiencia de estudio mediante inteligencia artificial. Estud.ia permite a los usuarios cargar documentos, generar resúmenes, crear cuestionarios interactivos y obtener respuestas contextualizadas mediante búsqueda semántica.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Microservicios](#-microservicios)
- [Contenedores Docker](#-contenedores-docker)
- [Configuración](#-configuración)
- [Ejecución](#-ejecución)
- [API Endpoints](#-api-endpoints)
- [Desarrollo](#-desarrollo)
- [Contribuidores](#-contribuidores)

## 🎯 Características

- **Procesamiento de Documentos**: Carga y procesamiento automático de PDFs y otros documentos
- **Generación de Embeddings**: Conversión de documentos en embeddings semánticos usando IA
- **Búsqueda Semántica**: Búsqueda inteligente en la base de datos vectorial
- **Generación de Resúmenes**: Resúmenes automáticos de documentos cargados
- **Cuestionarios Interactivos**: Generación automática de preguntas y respuestas
- **Tarjetas de Estudio (Flashcards)**: Creación de tarjetas para memorización
- **Sistema de Autenticación**: Autenticación con OAuth2 (Google) y credenciales locales
- **Chat RAG**: Interfaz de chat para interactuar con los documentos cargados
- **Gestión de Notebooks**: Organización de documentos en cuadernos virtuales

## 🛠 Tecnologías

### Frontend
- **Next.js 16** - Framework React moderno
- **React 19** - Librería de componentes
- **TypeScript** - Tipado estático para JavaScript
- **Tailwind CSS** - Framework CSS utility-first
- **Axios** - Cliente HTTP para solicitudes

### Backend - API Usuarios
- **FastAPI** - Framework web asincrónico
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **PostgreSQL** - Base de datos relacional
- **Python-jose** - Autenticación JWT
- **Authlib** - Integración OAuth2

### Backend - API Langchain
- **FastAPI** - Framework web asincrónico
- **LangChain** - Framework para aplicaciones con IA
- **Google Generative AI** - Modelos de Google para embeddings
- **Voyage AI** - Embeddings de alta calidad
- **LangMilvus** - Integración con base de datos vectorial
- **BeautifulSoup** - Parsing de documentos HTML
- **PyPDF** - Procesamiento de archivos PDF

### Almacenamiento
- **Milvus** - Base de datos vectorial de código abierto
- **PostgreSQL** - Base de datos relacional
- **MinIO** - Almacenamiento S3-compatible
- **etcd** - Almacenamiento clave-valor distribuido

## 📦 Requisitos Previos

- **Docker Desktop** (versión 20.10 o superior)
- **Docker Compose** (versión 1.29 o superior)
- **Git**
- **Node.js 18+** (para desarrollo local del frontend)
- **Python 3.12+** (para desarrollo local del backend)

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/IvanVijandi/Estud.ia.git
cd Estud.ia
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de Datos
DB_URL=postgresql://user:password@postgres:5432/estudia
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=estudia

# Autenticación
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# APIs Externas
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
VOYAGE_API_KEY=your-voyage-api-key

# URLs de Servicios
LANGCHAIN_URI=http://langchain:3000
MILVUS_URI=http://standalone:19530
ZILLIZ_URI=your-zilliz-uri
ZILLIZ_TOKEN=your-zilliz-token

# Docker
RESTART_POLICY=unless-stopped
DOCKER_VOLUME_DIRECTORY=./volumes
```

### 3. Construir e Iniciar Contenedores

```bash
docker-compose up -d
```

## 📂 Estructura del Proyecto

```
Estud.ia/
├── estud.ia/                    # Frontend Next.js
│   ├── app/                     # Componentes y páginas
│   │   ├── components/          # Componentes reutilizables
│   │   ├── contexts/            # React Contexts
│   │   ├── lib/                 # Utilidades y APIs
│   │   ├── login/               # Página de login
│   │   ├── register/            # Página de registro
│   │   └── notebook/            # Gestión de notebooks
│   ├── public/                  # Activos estáticos
│   └── package.json             # Dependencias de Node.js
│
├── UsersAPI/                    # Microservicio de Usuarios
│   ├── app/
│   │   ├── crud/                # Operaciones de base de datos
│   │   ├── models/              # Modelos SQLAlchemy
│   │   ├── routers/             # Rutas de API
│   │   ├── schemas/             # Esquemas Pydantic
│   │   ├── security/            # Autenticación y seguridad
│   │   └── utils/               # Funciones auxiliares
│   ├── migrations/              # Migraciones de base de datos
│   └── pyproject.toml           # Dependencias de Python
│
├── Langchain/                   # Microservicio RAG
│   ├── app/
│   │   ├── db/                  # Conexión a Milvus
│   │   ├── schemas/             # DTOs y esquemas
│   │   ├── security/            # Seguridad de API
│   │   ├── utils/               # Embeddings, splitting, reranking
│   │   └── main.py              # Punto de entrada
│   ├── test/                    # Tests unitarios
│   └── pyproject.toml           # Dependencias de Python
│
├── docker-compose.yml           # Definición de servicios
├── README.md                    # Este archivo
└── docs/                        # Documentación adicional
    └── postgres_database_diagram.mwb
```

## 🔧 Microservicios

### 1. **Frontend - Estud.ia (Next.js)**
- **Puerto**: 3000
- **Descripción**: Interfaz web para usuarios
- **Características**: 
  - Autenticación de usuarios
  - Carga de documentos
  - Visualización de notebooks
  - Chat RAG
  - Gestión de cuestionarios y tarjetas

### 2. **UsersAPI (FastAPI)**
- **Puerto**: 5000
- **Descripción**: API de gestión de usuarios y datos
- **Endpoints Principales**:
  - Autenticación (login, registro, OAuth)
  - Gestión de usuarios
  - CRUD de notebooks
  - CRUD de cuestionarios
  - CRUD de resúmenes
  - CRUD de flashcards
  - Gestión de mensajes

### 3. **LangchainAPI (FastAPI)**
- **Puerto**: 80
- **Descripción**: API de procesamiento de documentos y RAG
- **Funcionalidades**:
  - Procesamiento de PDFs
  - Generación de embeddings
  - Búsqueda semántica en Milvus
  - Generación de respuestas con IA
  - Splitting de documentos

## 🐳 Contenedores Docker

| Contenedor | Puerto(s) | Descripción | Imagen |
|--|--|--|--|
| **users-api** | 5000 | API FastAPI para gestión de usuarios | Construcción personalizada |
| **langchain** | 80 | API FastAPI para procesamiento RAG | Construcción personalizada |
| **postgres-users** | 5432 | Base de datos PostgreSQL | postgres:16-alpine |
| **milvus-etcd** | 2379 | Coordinación de Milvus | quay.io/coreos/etcd:v3.5.18 |
| **milvus-minio** | 9000, 9001 | Almacenamiento de objetos S3 | minio/minio:RELEASE.2024-12-18 |
| **milvus-standalone** | 19530, 9091 | Base de datos vectorial | milvusdb/milvus:latest |
| **attu** | 8001 | Panel de administración Milvus | webui de Milvus |

## ⚙️ Configuración

### Variables de Entorno Importantes

#### Autenticación
- `SECRET_KEY`: Clave secreta para JWT (generar con: `openssl rand -hex 32`)
- `ALGORITHM`: Algoritmo de firma (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Duración del token (30 minutos)

#### Base de Datos
- `DB_URL`: Conexión a PostgreSQL
- `POSTGRES_USER`: Usuario de PostgreSQL
- `POSTGRES_PASSWORD`: Contraseña de PostgreSQL

#### APIs Externas
- `GOOGLE_API_KEY`: Clave de API de Google Generative AI
- `GOOGLE_CLIENT_ID/SECRET`: Credenciales OAuth de Google
- `VOYAGE_API_KEY`: Clave de API de Voyage AI

#### Milvus
- `MILVUS_URI`: URL de conexión local o Zilliz Cloud
- `ZILLIZ_URI`: URI de Zilliz Cloud (alternativa)
- `ZILLIZ_TOKEN`: Token de Zilliz Cloud

## 🏃 Ejecución

### Iniciar Todos los Servicios

```bash
docker-compose up -d
```

### Ver Logs

```bash
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f [service-name]
```

### Detener Servicios

```bash
docker-compose down
```

### Recrear Contenedores

```bash
docker-compose up -d --build
```

## 📡 API Endpoints

> Accede a la documentación interactiva en `http://localhost:5000/docs` (UsersAPI) y `http://localhost:80/docs` (LangchainAPI) después de iniciar los contenedores.

### UsersAPI (Puerto 5000)

#### 🔐 Autenticación
- `GET /auth/me` - Obtener datos del usuario actual
- `POST /auth/login` - Login con credenciales (email/password)
- `POST /auth/register` - Registro de usuario
- `POST /auth/logout` - Cerrar sesión
- `GET /auth/login/google` - Iniciar flujo OAuth con Google
- `GET /auth/callback/google` - Callback de Google OAuth

#### 👤 Usuarios
- `POST /users/` - Crear nuevo usuario
- `GET /users/` - Listar usuarios (con paginación: skip, limit)
- `GET /users/{user_id}` - Obtener datos de usuario
- `GET /users/by_email/` - Obtener usuario por email
- `DELETE /users/{user_id}` - Eliminar usuario

#### 📓 Notebooks
- `POST /notebooks/` - Crear notebook con documentos
- `GET /notebooks/` - Listar todos los notebooks
- `GET /notebooks/{notebook_id}` - Obtener detalles del notebook
- `DELETE /notebooks/{notebook_id}` - Eliminar notebook
- `GET /notebooks/{notebook_id}/sources` - Obtener fuentes de un notebook
- `GET /notebooks/user/{user_id}` - Obtener notebooks de un usuario
- `POST /notebooks/{notebook_id}/sources` - Agregar documentos a notebook
- `POST /notebooks/{notebook_id}/flashcards` - Generar flashcards automáticamente
- `POST /notebooks/{notebook_id}/quiz` - Generar cuestionarios automáticamente
- `DELETE /notebooks/{notebook_id}/sources` - Eliminar múltiples fuentes

#### 📄 Fuentes (Documentos)
- `POST /sources/` - Crear nueva fuente
- `GET /sources/` - Listar todas las fuentes
- `GET /sources/{source_id}` - Obtener detalles de una fuente
- `DELETE /sources/{source_id}` - Eliminar una fuente
- `DELETE /sources/delete-various` - Eliminar múltiples fuentes por IDs
- `GET /sources/{source_id}/notebook` - Obtener notebook de una fuente

#### ❓ Cuestionarios
- `POST /quizzes/` - Crear cuestionario
- `GET /quizzes/` - Listar cuestionarios
- `GET /quizzes/{quiz_id}` - Obtener cuestionario
- `DELETE /quizzes/{quiz_id}` - Eliminar cuestionario
- `GET /quizzes/notebook/{notebook_id}` - Obtener quizzes de un notebook
- `GET /quizzes/user/{user_id}` - Obtener quizzes de un usuario

##### Preguntas de Cuestionarios
- `POST /quizzes/{quiz_id}/questions` - Agregar pregunta a cuestionario
- `GET /quizzes/{quiz_id}/questions` - Obtener preguntas de un cuestionario
- `DELETE /quizzes/questions/{question_id}` - Eliminar pregunta

#### 🎴 Flashcards
- `POST /flashcards/` - Crear flashcard
- `GET /flashcards/` - Listar flashcards
- `GET /flashcards/{flashcard_id}` - Obtener detalles de flashcard
- `DELETE /flashcards/{flashcard_id}` - Eliminar flashcard
- `GET /flashcards/notebook/{notebook_id}` - Obtener flashcards de un notebook
- `GET /flashcards/user/{user_id}` - Obtener flashcards de un usuario

#### 📝 Resúmenes
- `POST /summaries/` - Crear resumen
- `GET /summaries/` - Listar resúmenes
- `GET /summaries/{summary_id}` - Obtener resumen
- `DELETE /summaries/{summary_id}` - Eliminar resumen
- `GET /summaries/notebook/{notebook_id}` - Obtener resúmenes de un notebook
- `GET /summaries/user/{user_id}` - Obtener resúmenes de un usuario

#### 💬 Mensajes (Chat)
- `POST /messages/` - Crear mensaje (genérico)
- `POST /messages/user` - Crear mensaje enviado por usuario
- `POST /messages/llm` - Crear mensaje generado por IA (consulta a LangChain)
- `GET /messages/` - Listar mensajes (con paginación)
- `GET /messages/{message_id}` - Obtener mensaje
- `DELETE /messages/{message_id}` - Eliminar mensaje
- `GET /messages/notebook/{notebook_id}` - Obtener mensajes de un notebook
- `GET /messages/user/` - Obtener mensajes del usuario actual

### LangchainAPI (Puerto: 80)

> Esta API maneja el procesamiento de documentos, generación de embeddings y búsqueda semántica con la base de datos vectorial Milvus.

#### 📤 Procesamiento de Documentos
- `POST /upload-pdf` - Subir y procesar documento PDF
- `POST /delete-pdfs` - Eliminar documentos de la base vectorial
- `POST /search` - Búsqueda semántica en documentos

#### 💭 Chat y Generación de Contenido
- `POST /chat` - Enviar consulta al chat RAG y obtener respuesta generada
- `POST /generate-summary` - Generar resumen de documento
- `POST /generate-quiz` - Generar cuestionario de documento
- `POST /generate-flashcards` - Generar flashcards de documento

## 👨‍💻 Desarrollo

### Configurar Entorno Local

#### Frontend (estud.ia/)
```bash
cd estud.ia
npm install
npm run dev
# Acceder en http://localhost:3000
```

#### UsersAPI
```bash
cd UsersAPI
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e .
python app/main.py
# Acceder en http://localhost:5000/docs
```

#### LangchainAPI
```bash
cd Langchain
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e .
python app/main.py
# Acceder en http://localhost:80/docs
```


### Linting y Formateo

Frontend:
```bash
cd estud.ia
npm run lint
```

## 🤝 Contribuidores

- **Franco Pientrantuono**
- **Ivan Vijandi**

## 📝 Licencia

Este proyecto está bajo licencia [MIT/Apache 2.0 - Especificar aquí]

## 📞 Contacto y Soporte

Para reportar problemas o sugerencias, por favor crea un issue en el repositorio.

---

**Última actualización**: Febrero 2026