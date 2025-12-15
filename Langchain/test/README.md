# Tests Unitarios - Langchain

Este directorio contiene los tests unitarios para los módulos principales de la aplicación Langchain.

## Estructura

- `test_embeddings.py` - Tests para el módulo de generación de embeddings
- `test_splitter.py` - Tests para el módulo de división de documentos
- `test_milvus.py` - Tests para las funciones de Milvus (upload y search)

## Ejecutar los tests

### Todos los tests

```bash
# Desde el directorio Langchain
python -m unittest discover -s test -p "test_*.py" -v
```

### Test individual

```bash
# Test de embeddings
python -m unittest test.test_embeddings -v

# Test de splitter
python -m unittest test.test_splitter -v

# Test de milvus
python -m unittest test.test_milvus -v
```

### Test específico

```bash
# Ejecutar un método de test específico
python -m unittest test.test_embeddings.TestEmbeddingGenerator.test_format_database -v
```

## Cobertura de tests

### test_embeddings.py
- ✅ Inicialización del generador
- ✅ Generación de embeddings de documentos
- ✅ Generación de embeddings de consultas
- ✅ Formateo de datos para base de datos
- ✅ Manejo de listas vacías
- ✅ Manejo de listas desbalanceadas

### test_splitter.py
- ✅ Inicialización del splitter
- ✅ División de documentos PDF válidos
- ✅ Estructura de chunks generados
- ✅ Preservación de metadatos
- ✅ Manejo de PDFs vacíos
- ✅ Procesamiento de múltiples páginas

### test_milvus.py
- ✅ Subida de documentos
- ✅ Subida de datos vacíos
- ✅ Búsqueda de documentos
- ✅ Búsqueda con filtros
- ✅ Búsqueda sin resultados
- ✅ Eliminación de colecciones
- ✅ Creación de colecciones nuevas
- ✅ Manejo de colecciones existentes
- ✅ Flujo completo de integración

## Requisitos

Los tests utilizan mocks para evitar dependencias externas (Google API, Milvus, etc.). No es necesario tener servicios corriendo para ejecutar los tests.

## Notas

- Los tests utilizan `unittest.mock` para simular dependencias externas
- Los métodos asíncronos se ejecutan con `asyncio.run()`
- Se verifican tanto casos de éxito como casos edge
